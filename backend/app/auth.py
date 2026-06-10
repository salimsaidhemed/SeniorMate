from functools import wraps

import jwt
from flask import current_app, g, jsonify, request


ROLE_PERMISSIONS = {
    "admin": {"*"},
    "manager": {
        "patients.read",
        "patients.write",
        "visits.read",
        "visits.write",
        "aide_notes.read",
        "aide_notes.write",
        "nurse_notes.read",
        "nurse_notes.write",
        "assessments.read",
        "assessments.write",
        "medical_records.read",
        "medical_records.write",
        "patient_photos.read",
        "patient_photos.write",
        "patient_photos.verify",
        "dashboard.read",
        "reports.read",
        "branding.read",
        "branding.write",
    },
    "nurse": {
        "patients.read",
        "visits.read",
        "visits.write",
        "aide_notes.read",
        "nurse_notes.read",
        "nurse_notes.write",
        "assessments.read",
        "assessments.write",
        "medical_records.read",
        "medical_records.write",
        "patient_photos.read",
        "dashboard.read",
        "reports.read",
        "branding.read",
    },
    "caregiver": {
        "patients.read",
        "visits.read",
        "aide_notes.read",
        "aide_notes.write",
        "nurse_notes.read",
        "assessments.read",
        "medical_records.read",
        "patient_photos.read",
        "reports.read",
        "branding.read",
    },
    "viewer": {
        "patients.read",
        "visits.read",
        "aide_notes.read",
        "nurse_notes.read",
        "assessments.read",
        "medical_records.read",
        "patient_photos.read",
        "dashboard.read",
        "reports.read",
        "branding.read",
    },
}

PUBLIC_API_PATHS = {
    "/api/health",
    "/api/docs",
    "/api/openapi.json",
}

_jwks_clients = {}


def extract_roles(claims):
    roles = set(claims.get("realm_access", {}).get("roles", []))
    audience = current_app.config.get("KEYCLOAK_AUDIENCE", "seniormate-api")
    roles.update(
        claims.get("resource_access", {}).get(audience, {}).get("roles", [])
    )
    return sorted(role for role in roles if role in ROLE_PERMISSIONS)


def decode_access_token(token):
    jwks_url = current_app.config["KEYCLOAK_JWKS_URL"]
    client = _jwks_clients.setdefault(jwks_url, jwt.PyJWKClient(jwks_url))
    signing_key = client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=current_app.config["KEYCLOAK_AUDIENCE"],
        issuer=current_app.config["KEYCLOAK_ISSUER"],
    )


def get_current_user():
    return getattr(g, "current_user", None)


def _development_user():
    return {
        "id": "development-user",
        "username": "development",
        "name": "Development User",
        "email": None,
        "roles": ["admin"],
        "claims": {},
    }


def _user_from_claims(claims):
    return {
        "id": claims.get("sub"),
        "username": claims.get("preferred_username"),
        "name": claims.get("name") or claims.get("preferred_username"),
        "email": claims.get("email"),
        "roles": extract_roles(claims),
        "claims": claims,
    }


def _authentication_error(message):
    return jsonify({"message": message}), 401


def authenticate_request():
    if get_current_user():
        return None

    if not current_app.config.get("AUTH_ENABLED", False):
        g.current_user = _development_user()
        return None

    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return _authentication_error("Authentication required")

    try:
        claims = decode_access_token(token)
    except (
        jwt.PyJWTError,
        jwt.PyJWKClientError,
        ValueError,
        TypeError,
    ):
        return _authentication_error("Invalid or expired access token")

    g.current_user = _user_from_claims(claims)
    return None


def _resource_for_path(path):
    if path.startswith("/api/settings/branding"):
        return "branding"
    if path.startswith("/api/dashboard"):
        return "dashboard"
    if "/medical-records" in path:
        return "medical_records"
    if "/aide-notes" in path or "/aide-note" in path:
        return "aide_notes"
    if "/nurse-notes" in path or "/nurse-note" in path:
        return "nurse_notes"
    if "/assessments" in path:
        return "assessments"
    if "/visits" in path:
        return "visits"
    if path.startswith("/api/patients") and "/photo" in path:
        return "patient_photos"
    if path.startswith("/api/patients"):
        return "patients"
    return None


def _required_permission(path, method):
    resource = _resource_for_path(path)
    if not resource:
        return None
    if resource == "patient_photos" and path.endswith("/verify"):
        return "patient_photos.verify"
    action = "read" if method in {"GET", "HEAD"} else "write"
    return f"{resource}.{action}"


def user_has_permission(user, permission):
    if not permission:
        return False
    permissions = set()
    for role in user.get("roles", []):
        permissions.update(ROLE_PERMISSIONS.get(role, set()))
    return "*" in permissions or permission in permissions


def protect_api_request():
    if not request.path.startswith("/api/"):
        return None
    if (
        request.method == "OPTIONS"
        or request.path in PUBLIC_API_PATHS
        or request.path.startswith("/api/public/branding")
    ):
        return None

    error = authenticate_request()
    if error:
        return error
    if not current_app.config.get("AUTH_ENABLED", False):
        return None

    permission = _required_permission(request.path, request.method)
    if not user_has_permission(get_current_user(), permission):
        return jsonify({"message": "Insufficient permissions"}), 403
    return None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        error = authenticate_request()
        if error:
            return error
        return view(*args, **kwargs)

    return wrapped


def roles_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            error = authenticate_request()
            if error:
                return error
            roles = set(get_current_user().get("roles", []))
            if not roles.intersection(allowed_roles):
                return jsonify({"message": "Insufficient permissions"}), 403
            return view(*args, **kwargs)

        return wrapped

    return decorator
