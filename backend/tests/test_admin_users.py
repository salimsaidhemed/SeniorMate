from copy import deepcopy


class FakeKeycloakAdminClient:
    def __init__(self):
        self.users = {
            "user-1": {
                "id": "user-1",
                "username": "nurse.demo",
                "email": "nurse.demo@example.test",
                "first_name": "Nurse",
                "last_name": "Demo",
                "enabled": True,
                "email_verified": True,
                "roles": ["nurse"],
            }
        }
        self.password_resets = []

    def list_users(self):
        return deepcopy(list(self.users.values()))

    def get_user(self, user_id):
        return deepcopy(self.users[user_id])

    def create_user(self, data):
        user = {
            "id": "user-2",
            **{
                key: data.get(key)
                for key in (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "enabled",
                    "email_verified",
                    "roles",
                )
            },
        }
        self.users[user["id"]] = user
        return deepcopy(user)

    def update_user(self, user_id, data):
        self.users[user_id].update(data)
        return deepcopy(self.users[user_id])

    def set_enabled(self, user_id, enabled):
        self.users[user_id]["enabled"] = enabled
        return deepcopy(self.users[user_id])

    def delete_user(self, user_id):
        del self.users[user_id]

    def reset_password(self, user_id, password, temporary=True):
        self.password_resets.append((user_id, password, temporary))

    def list_roles(self):
        return ["admin", "caregiver", "manager", "nurse", "viewer"]

    def update_user_roles(self, user_id, roles):
        self.users[user_id]["roles"] = roles
        return deepcopy(self.users[user_id])


def auth_claims(role):
    return {
        "sub": f"{role}-user",
        "preferred_username": f"{role}.demo",
        "realm_access": {"roles": [role]},
    }


def enable_auth(app, monkeypatch, role=None):
    app.config["AUTH_ENABLED"] = True
    if role:
        monkeypatch.setattr(
            "app.auth.decode_access_token",
            lambda _token: auth_claims(role),
        )


def auth_header():
    return {"Authorization": "Bearer test-token"}


def valid_user_payload():
    return {
        "username": "alex.morgan",
        "email": "alex.morgan@example.test",
        "first_name": "Alex",
        "last_name": "Morgan",
        "password": "temporary-password",
        "roles": ["caregiver"],
    }


def test_unauthenticated_user_management_is_blocked(app, client):
    app.config["AUTH_ENABLED"] = True

    response = client.get("/api/admin/users")

    assert response.status_code == 401


def test_non_admin_user_management_is_blocked(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "manager")

    response = client.get("/api/admin/users", headers=auth_header())

    assert response.status_code == 403


def test_admin_can_list_users(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "admin")

    response = client.get("/api/admin/users", headers=auth_header())

    assert response.status_code == 200
    assert response.get_json()["data"][0]["username"] == "nurse.demo"


def test_admin_can_create_user(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "admin")

    response = client.post(
        "/api/admin/users",
        json=valid_user_payload(),
        headers=auth_header(),
    )

    assert response.status_code == 201
    assert response.get_json()["data"]["roles"] == ["caregiver"]


def test_admin_can_update_user(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "admin")

    response = client.put(
        "/api/admin/users/user-1",
        json={
            "username": "nurse.updated",
            "email": "updated@example.test",
            "first_name": "Updated",
        },
        headers=auth_header(),
    )

    assert response.status_code == 200
    assert response.get_json()["data"]["username"] == "nurse.updated"
    assert response.get_json()["data"]["last_name"] == "Demo"


def test_admin_can_disable_user(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "admin")

    response = client.patch(
        "/api/admin/users/user-1/enabled",
        json={"enabled": False},
        headers=auth_header(),
    )

    assert response.status_code == 200
    assert response.get_json()["data"]["enabled"] is False


def test_admin_can_assign_roles(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "admin")

    response = client.put(
        "/api/admin/users/user-1/roles",
        json={"roles": ["manager", "nurse"]},
        headers=auth_header(),
    )

    assert response.status_code == 200
    assert response.get_json()["data"]["roles"] == ["manager", "nurse"]


def test_invalid_role_is_rejected(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "admin")

    response = client.put(
        "/api/admin/users/user-1/roles",
        json={"roles": ["superuser"]},
        headers=auth_header(),
    )

    assert response.status_code == 400
    assert "Unsupported roles" in response.get_json()["errors"]["roles"]


def test_auth_disabled_allows_local_user_management(client):
    response = client.get("/api/admin/users")

    assert response.status_code == 200


def test_admin_can_reset_temporary_password(
    app,
    client,
    monkeypatch,
    keycloak_admin_client,
):
    enable_auth(app, monkeypatch, "admin")

    response = client.post(
        "/api/admin/users/user-1/reset-password",
        json={"password": "new-temporary-password", "temporary": True},
        headers=auth_header(),
    )

    assert response.status_code == 200
    assert keycloak_admin_client.password_resets == [
        ("user-1", "new-temporary-password", True)
    ]
