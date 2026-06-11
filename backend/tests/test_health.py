def test_create_app(app):
    assert app is not None
    assert app.config["TESTING"] is True


def test_health_endpoint_returns_success(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
    assert response.get_json()["database"] == "ok"
    assert response.get_json()["version"] == "1.0.0"
