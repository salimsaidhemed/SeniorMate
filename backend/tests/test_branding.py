from io import BytesIO


VALID_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
<rect width="40" height="40" fill="#1F6F68"/>
</svg>"""


def auth_claims(role):
    return {
        "sub": "branding-user",
        "preferred_username": f"{role}.demo",
        "realm_access": {"roles": [role]},
    }


def enable_auth(app, monkeypatch, role):
    app.config["AUTH_ENABLED"] = True
    monkeypatch.setattr(
        "app.auth.decode_access_token",
        lambda _token: auth_claims(role),
    )


def auth_header():
    return {"Authorization": "Bearer test-token"}


def test_get_default_branding(client):
    response = client.get("/api/settings/branding")
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["app_display_name"] == "SeniorMate"
    assert data["primary_color"] == "#1F6F68"
    assert data["has_custom_logo"] is False
    assert data["logo_url"] is None


def test_update_branding(client):
    response = client.put(
        "/api/settings/branding",
        json={
            "organization_name": "Harbor Care",
            "app_display_name": "HarborMate",
            "primary_color": "#236B63",
            "secondary_color": "#486B78",
            "accent_color": "#3A8179",
            "sidebar_color": "#F7FAF9",
            "login_banner_text": "Welcome to Harbor Care.",
            "footer_text": "Harbor Care clinical operations",
        },
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["organization_name"] == "Harbor Care"
    assert data["app_display_name"] == "HarborMate"
    assert data["primary_color"] == "#236B63"


def test_update_branding_rejects_invalid_color(client):
    response = client.put(
        "/api/settings/branding",
        json={"primary_color": "teal"},
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["primary_color"].startswith(
        "Use a six-digit hex color"
    )


def test_upload_valid_logo(client, branding_logo_storage):
    response = client.post(
        "/api/settings/branding/logo",
        data={
            "file": (BytesIO(VALID_SVG), "harbor-care.svg", "image/svg+xml"),
        },
        content_type="multipart/form-data",
    )
    data = response.get_json()["data"]

    assert response.status_code == 201
    assert data["has_custom_logo"] is True
    assert data["logo_url"] == "/api/public/branding/logo"
    assert len(branding_logo_storage.objects) == 1
    assert next(iter(branding_logo_storage.objects)).startswith(
        "branding/default/logo/"
    )


def test_upload_rejects_invalid_logo_type(client):
    response = client.post(
        "/api/settings/branding/logo",
        data={
            "file": (
                BytesIO(b"<html>not a logo</html>"),
                "logo.html",
                "text/html",
            ),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == (
        "Use an SVG, PNG, or JPEG logo."
    )


def test_upload_rejects_unsafe_svg(client):
    response = client.post(
        "/api/settings/branding/logo",
        data={
            "file": (
                BytesIO(b"<svg><script>alert(1)</script></svg>"),
                "unsafe.svg",
                "image/svg+xml",
            ),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["file"] == (
        "Logo content is invalid or unsafe."
    )


def test_delete_logo(client, branding_logo_storage):
    client.post(
        "/api/settings/branding/logo",
        data={
            "file": (BytesIO(VALID_SVG), "harbor-care.svg", "image/svg+xml"),
        },
        content_type="multipart/form-data",
    )

    response = client.delete("/api/settings/branding/logo")

    assert response.status_code == 200
    assert response.get_json()["data"]["has_custom_logo"] is False
    assert branding_logo_storage.objects == {}


def test_public_branding_returns_safe_data(client):
    client.put(
        "/api/settings/branding",
        json={"organization_name": "Harbor Care"},
    )
    client.post(
        "/api/settings/branding/logo",
        data={
            "file": (BytesIO(VALID_SVG), "harbor-care.svg", "image/svg+xml"),
        },
        content_type="multipart/form-data",
    )

    response = client.get("/api/public/branding")
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["organization_name"] == "Harbor Care"
    assert data["logo_url"] == "/api/public/branding/logo"
    assert "logo_object_key" not in data
    assert "storage_bucket" not in data


def test_public_logo_streams_private_object(client):
    client.post(
        "/api/settings/branding/logo",
        data={
            "file": (BytesIO(VALID_SVG), "harbor-care.svg", "image/svg+xml"),
        },
        content_type="multipart/form-data",
    )

    response = client.get("/api/public/branding/logo")

    assert response.status_code == 200
    assert response.data == VALID_SVG
    assert response.mimetype == "image/svg+xml"


def test_viewer_cannot_update_branding(app, client, monkeypatch):
    enable_auth(app, monkeypatch, "viewer")

    response = client.put(
        "/api/settings/branding",
        json={"organization_name": "Blocked"},
        headers=auth_header(),
    )

    assert response.status_code == 403


def test_admin_and_manager_can_update_branding(app, client, monkeypatch):
    for role in ("admin", "manager"):
        enable_auth(app, monkeypatch, role)
        response = client.put(
            "/api/settings/branding",
            json={"organization_name": f"{role.title()} Care"},
            headers=auth_header(),
        )
        assert response.status_code == 200


def test_public_branding_remains_public_when_auth_enabled(app, client):
    app.config["AUTH_ENABLED"] = True

    response = client.get("/api/public/branding")

    assert response.status_code == 200
