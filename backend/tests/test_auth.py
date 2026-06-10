from app.auth import extract_roles


def token_claims(*roles):
    return {
        "sub": "user-123",
        "preferred_username": "sam",
        "name": "Sam Care",
        "email": "sam@example.com",
        "realm_access": {"roles": list(roles)},
    }


def enable_auth(app, monkeypatch, claims=None, error=None):
    app.config["AUTH_ENABLED"] = True

    def decode(_token):
        if error:
            raise error
        return claims or token_claims("viewer")

    monkeypatch.setattr("app.auth.decode_access_token", decode)


def test_health_remains_public_when_auth_is_enabled(app, client):
    app.config["AUTH_ENABLED"] = True

    response = client.get("/api/health")

    assert response.status_code == 200


def test_protected_endpoint_requires_token(app, client):
    app.config["AUTH_ENABLED"] = True

    response = client.get("/api/patients")

    assert response.status_code == 401
    assert response.get_json()["message"] == "Authentication required"


def test_invalid_token_returns_unauthorized(app, client, monkeypatch):
    enable_auth(app, monkeypatch, error=ValueError("invalid token"))

    response = client.get(
        "/api/patients",
        headers={"Authorization": "Bearer invalid"},
    )

    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid or expired access token"


def test_insufficient_role_returns_forbidden(app, client, monkeypatch):
    enable_auth(app, monkeypatch, token_claims("viewer"))

    response = client.post(
        "/api/patients",
        json={"first_name": "Maria", "last_name": "Santos"},
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Insufficient permissions"


def test_allowed_role_can_create_patient(app, client, monkeypatch):
    enable_auth(app, monkeypatch, token_claims("manager"))

    response = client.post(
        "/api/patients",
        json={"first_name": "Maria", "last_name": "Santos"},
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 201


def test_auth_disabled_preserves_local_development_behavior(client):
    response = client.get("/api/patients")

    assert response.status_code == 200


def test_extract_roles_combines_realm_and_api_client_roles(app):
    claims = {
        "realm_access": {"roles": ["viewer", "offline_access"]},
        "resource_access": {
            "seniormate-api": {"roles": ["nurse"]},
        },
    }

    with app.app_context():
        assert extract_roles(claims) == ["nurse", "viewer"]
