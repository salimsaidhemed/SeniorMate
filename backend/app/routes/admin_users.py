from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.keycloak_admin import (
    KeycloakAdminError,
    SENIORMATE_ROLES,
    get_keycloak_admin_client,
)
from app.swagger import (
    admin_role_list_spec,
    admin_user_create_spec,
    admin_user_delete_spec,
    admin_user_enabled_spec,
    admin_user_get_spec,
    admin_user_list_spec,
    admin_user_reset_password_spec,
    admin_user_roles_spec,
    admin_user_update_spec,
)


admin_users_bp = Blueprint("admin_users", __name__, url_prefix="/api/admin")
USER_FIELDS = {
    "username",
    "email",
    "first_name",
    "last_name",
    "enabled",
    "email_verified",
}


def success_response(data, message, status_code=200):
    return jsonify({"data": data, "message": message}), status_code


def error_response(message, status_code=400, errors=None):
    payload = {"message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status_code


def admin_client_call(action):
    try:
        return action()
    except KeycloakAdminError as exc:
        return error_response(str(exc), exc.status_code)


def validate_roles(roles):
    if roles is None:
        return [], None
    if not isinstance(roles, list) or not all(isinstance(role, str) for role in roles):
        return None, "Roles must be an array."
    invalid = sorted(set(roles) - set(SENIORMATE_ROLES))
    if invalid:
        return None, f"Unsupported roles: {', '.join(invalid)}."
    return sorted(set(roles)), None


def validate_user_payload(payload, creating=False):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}
    data = {}
    errors = {}
    for field in USER_FIELDS:
        if field in payload:
            value = payload[field]
            if isinstance(value, str):
                value = value.strip()
            data[field] = value

    for field in ("username", "email"):
        if creating and not data.get(field):
            errors[field] = "This field is required."
    if creating and not payload.get("password"):
        errors["password"] = "This field is required."
    if data.get("email") and "@" not in data["email"]:
        errors["email"] = "Enter a valid email address."
    for field in ("enabled", "email_verified"):
        if field in data and not isinstance(data[field], bool):
            errors[field] = "This field must be true or false."

    roles, role_error = validate_roles(payload.get("roles"))
    if role_error:
        errors["roles"] = role_error
    elif "roles" in payload:
        data["roles"] = roles

    if creating:
        data["password"] = payload.get("password")
        temporary = payload.get("temporary_password", True)
        if not isinstance(temporary, bool):
            errors["temporary_password"] = "This field must be true or false."
        data["temporary_password"] = temporary
        data.setdefault("enabled", True)
        data.setdefault("email_verified", False)
        data.setdefault("roles", [])

    return data, errors


@admin_users_bp.get("/users")
@swag_from(admin_user_list_spec)
def list_users():
    result = admin_client_call(
        lambda: success_response(
            get_keycloak_admin_client().list_users(),
            "Users retrieved successfully",
        )
    )
    return result


@admin_users_bp.get("/users/<string:user_id>")
@swag_from(admin_user_get_spec)
def get_user(user_id):
    return admin_client_call(
        lambda: success_response(
            get_keycloak_admin_client().get_user(user_id),
            "User retrieved successfully",
        )
    )


@admin_users_bp.post("/users")
@swag_from(admin_user_create_spec)
def create_user():
    data, errors = validate_user_payload(request.get_json(silent=True), creating=True)
    if errors:
        return error_response("Invalid user data", 400, errors)
    return admin_client_call(
        lambda: success_response(
            get_keycloak_admin_client().create_user(data),
            "User created successfully",
            201,
        )
    )


@admin_users_bp.put("/users/<string:user_id>")
@swag_from(admin_user_update_spec)
def update_user(user_id):
    payload = request.get_json(silent=True)
    data, errors = validate_user_payload(payload)
    if errors:
        return error_response("Invalid user data", 400, errors)
    current = admin_client_call(
        lambda: get_keycloak_admin_client().get_user(user_id)
    )
    if isinstance(current, tuple):
        return current
    merged = {field: current.get(field) for field in USER_FIELDS}
    merged.update(data)
    return admin_client_call(
        lambda: success_response(
            get_keycloak_admin_client().update_user(user_id, merged),
            "User updated successfully",
        )
    )


@admin_users_bp.patch("/users/<string:user_id>/enabled")
@swag_from(admin_user_enabled_spec)
def set_user_enabled(user_id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("enabled"), bool):
        return error_response(
            "Invalid enabled state",
            400,
            {"enabled": "This field must be true or false."},
        )
    enabled = payload["enabled"]
    action = "enabled" if enabled else "disabled"
    return admin_client_call(
        lambda: success_response(
            get_keycloak_admin_client().set_enabled(user_id, enabled),
            f"User {action} successfully",
        )
    )


@admin_users_bp.delete("/users/<string:user_id>")
@swag_from(admin_user_delete_spec)
def delete_user(user_id):
    def delete():
        get_keycloak_admin_client().delete_user(user_id)
        return success_response({"id": user_id}, "User deleted successfully")

    return admin_client_call(delete)


@admin_users_bp.post("/users/<string:user_id>/reset-password")
@swag_from(admin_user_reset_password_spec)
def reset_user_password(user_id):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not payload.get("password"):
        return error_response(
            "Invalid password reset",
            400,
            {"password": "This field is required."},
        )
    temporary = payload.get("temporary", True)
    if not isinstance(temporary, bool):
        return error_response(
            "Invalid password reset",
            400,
            {"temporary": "This field must be true or false."},
        )

    def reset():
        get_keycloak_admin_client().reset_password(
            user_id,
            payload["password"],
            temporary,
        )
        return success_response(
            {"id": user_id, "temporary": temporary},
            "Password reset successfully",
        )

    return admin_client_call(reset)


@admin_users_bp.get("/roles")
@swag_from(admin_role_list_spec)
def list_roles():
    return admin_client_call(
        lambda: success_response(
            get_keycloak_admin_client().list_roles(),
            "Roles retrieved successfully",
        )
    )


@admin_users_bp.put("/users/<string:user_id>/roles")
@swag_from(admin_user_roles_spec)
def update_user_roles(user_id):
    payload = request.get_json(silent=True)
    roles, error = validate_roles(payload.get("roles") if isinstance(payload, dict) else None)
    if error or not isinstance(payload, dict) or "roles" not in payload:
        return error_response(
            "Invalid role assignment",
            400,
            {"roles": error or "This field is required."},
        )
    return admin_client_call(
        lambda: success_response(
            get_keycloak_admin_client().update_user_roles(user_id, roles),
            "User roles updated successfully",
        )
    )
