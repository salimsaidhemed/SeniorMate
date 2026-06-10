import time
from urllib.parse import quote

import httpx
from flask import current_app


SENIORMATE_ROLES = ("admin", "manager", "nurse", "caregiver", "viewer")


class KeycloakAdminError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


class KeycloakAdminClient:
    def __init__(
        self,
        base_url,
        realm,
        client_id,
        client_secret,
        http_client=None,
    ):
        self.base_url = base_url.rstrip("/")
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.http = http_client or httpx.Client(timeout=10.0)
        self._access_token = None
        self._token_expires_at = 0

    @property
    def realm_path(self):
        return f"/admin/realms/{quote(self.realm, safe='')}"

    def _token(self):
        if self._access_token and time.monotonic() < self._token_expires_at:
            return self._access_token
        try:
            response = self.http.post(
                f"{self.base_url}/realms/{quote(self.realm, safe='')}"
                "/protocol/openid-connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
        except httpx.HTTPError as exc:
            raise KeycloakAdminError(
                "Keycloak Admin API is unavailable."
            ) from exc
        if response.status_code != 200:
            raise KeycloakAdminError(
                "Keycloak Admin API authentication failed.",
                502,
            )
        payload = response.json()
        self._access_token = payload.get("access_token")
        if not self._access_token:
            raise KeycloakAdminError(
                "Keycloak did not return an admin access token."
            )
        self._token_expires_at = time.monotonic() + max(
            int(payload.get("expires_in", 60)) - 30,
            1,
        )
        return self._access_token

    def _request(self, method, path, *, json=None, params=None, expected=(200,)):
        try:
            response = self.http.request(
                method,
                f"{self.base_url}{path}",
                headers={"Authorization": f"Bearer {self._token()}"},
                json=json,
                params=params,
            )
        except httpx.HTTPError as exc:
            raise KeycloakAdminError(
                "Keycloak Admin API is unavailable."
            ) from exc
        if response.status_code not in expected:
            self._raise_for_response(response)
        if response.status_code == 204 or not response.content:
            return None, response
        return response.json(), response

    @staticmethod
    def _raise_for_response(response):
        detail = ""
        try:
            payload = response.json()
            detail = payload.get("errorMessage") or payload.get("error") or ""
        except ValueError:
            pass
        if response.status_code == 404:
            raise KeycloakAdminError("Keycloak user not found.", 404)
        if response.status_code == 409:
            raise KeycloakAdminError(
                detail or "A user with this username or email already exists.",
                409,
            )
        if response.status_code in {400, 422}:
            raise KeycloakAdminError(
                detail or "Keycloak rejected the user data.",
                400,
            )
        if response.status_code in {401, 403}:
            raise KeycloakAdminError(
                "Keycloak Admin API credentials lack required permissions.",
                502,
            )
        raise KeycloakAdminError(
            detail or "Keycloak Admin API request failed.",
            502,
        )

    @staticmethod
    def _user_payload(user):
        return {
            "id": user.get("id"),
            "username": user.get("username"),
            "email": user.get("email"),
            "first_name": user.get("firstName"),
            "last_name": user.get("lastName"),
            "enabled": user.get("enabled", True),
            "email_verified": user.get("emailVerified", False),
        }

    def _role_map(self):
        roles, _ = self._request("GET", f"{self.realm_path}/roles")
        return {
            role["name"]: role
            for role in roles
            if role.get("name") in SENIORMATE_ROLES
        }

    def _user_roles(self, user_id):
        roles, _ = self._request(
            "GET",
            f"{self.realm_path}/users/{quote(user_id, safe='')}/role-mappings/realm",
        )
        return sorted(
            role["name"]
            for role in roles
            if role.get("name") in SENIORMATE_ROLES
        )

    def list_users(self):
        users, _ = self._request(
            "GET",
            f"{self.realm_path}/users",
            params={"max": 500},
        )
        result = []
        for user in users:
            item = self._user_payload(user)
            item["roles"] = self._user_roles(user["id"])
            result.append(item)
        return result

    def get_user(self, user_id):
        user, _ = self._request(
            "GET",
            f"{self.realm_path}/users/{quote(user_id, safe='')}",
        )
        item = self._user_payload(user)
        item["roles"] = self._user_roles(user_id)
        return item

    def create_user(self, data):
        payload = {
            "username": data["username"],
            "email": data["email"],
            "firstName": data.get("first_name"),
            "lastName": data.get("last_name"),
            "enabled": data.get("enabled", True),
            "emailVerified": data.get("email_verified", False),
            "credentials": [
                {
                    "type": "password",
                    "value": data["password"],
                    "temporary": data.get("temporary_password", True),
                }
            ],
        }
        _, response = self._request(
            "POST",
            f"{self.realm_path}/users",
            json=payload,
            expected=(201,),
        )
        user_id = response.headers["Location"].rstrip("/").rsplit("/", 1)[-1]
        self.update_user_roles(user_id, data.get("roles", []))
        return self.get_user(user_id)

    def update_user(self, user_id, data):
        payload = {
            "username": data["username"],
            "email": data["email"],
            "firstName": data.get("first_name"),
            "lastName": data.get("last_name"),
            "enabled": data.get("enabled", True),
            "emailVerified": data.get("email_verified", False),
        }
        self._request(
            "PUT",
            f"{self.realm_path}/users/{quote(user_id, safe='')}",
            json=payload,
            expected=(204,),
        )
        return self.get_user(user_id)

    def set_enabled(self, user_id, enabled):
        self._request(
            "PUT",
            f"{self.realm_path}/users/{quote(user_id, safe='')}",
            json={"enabled": enabled},
            expected=(204,),
        )
        return self.get_user(user_id)

    def delete_user(self, user_id):
        self._request(
            "DELETE",
            f"{self.realm_path}/users/{quote(user_id, safe='')}",
            expected=(204,),
        )

    def reset_password(self, user_id, password, temporary=True):
        self._request(
            "PUT",
            f"{self.realm_path}/users/{quote(user_id, safe='')}/reset-password",
            json={
                "type": "password",
                "value": password,
                "temporary": temporary,
            },
            expected=(204,),
        )

    def list_roles(self):
        return sorted(self._role_map())

    def update_user_roles(self, user_id, desired_roles):
        role_map = self._role_map()
        assigned, _ = self._request(
            "GET",
            f"{self.realm_path}/users/{quote(user_id, safe='')}/role-mappings/realm",
        )
        current = {
            role["name"]: role
            for role in assigned
            if role.get("name") in SENIORMATE_ROLES
        }
        desired = set(desired_roles)
        remove = [current[name] for name in current.keys() - desired]
        add = [role_map[name] for name in desired - current.keys()]
        path = (
            f"{self.realm_path}/users/{quote(user_id, safe='')}"
            "/role-mappings/realm"
        )
        if remove:
            self._request("DELETE", path, json=remove, expected=(204,))
        if add:
            self._request("POST", path, json=add, expected=(204,))
        return self.get_user(user_id)


def get_keycloak_admin_client():
    client = current_app.extensions.get("keycloak_admin_client")
    if client is None:
        client = KeycloakAdminClient(
            current_app.config["KEYCLOAK_BASE_URL"],
            current_app.config["KEYCLOAK_REALM"],
            current_app.config["KEYCLOAK_ADMIN_CLIENT_ID"],
            current_app.config["KEYCLOAK_ADMIN_CLIENT_SECRET"],
        )
        current_app.extensions["keycloak_admin_client"] = client
    return client
