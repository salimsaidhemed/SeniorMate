def test_swagger_ui_is_reachable(client):
    response = client.get("/api/docs")

    assert response.status_code == 200
    assert b"swagger-ui" in response.data


def test_openapi_json_is_reachable(client):
    response = client.get("/api/openapi.json")
    body = response.get_json()

    assert response.status_code == 200
    assert body["info"]["title"] == "SeniorMate API"
    assert body["swagger"] == "2.0"


def test_openapi_json_includes_health_and_patient_endpoints(client):
    response = client.get("/api/openapi.json")
    paths = response.get_json()["paths"]

    assert "/api/health" in paths
    assert "/api/patients" in paths
    assert "/api/patients/{patient_id}" in paths
    assert "get" in paths["/api/health"]
    assert {"get", "post"} <= set(paths["/api/patients"].keys())
    assert {"get", "put", "delete"} <= set(
        paths["/api/patients/{patient_id}"].keys()
    )


def test_openapi_json_includes_patient_schemas(client):
    response = client.get("/api/openapi.json")
    definitions = response.get_json()["definitions"]

    assert "Patient" in definitions
    assert "PatientCreate" in definitions
    assert "PatientUpdate" in definitions
    assert "ErrorResponse" in definitions
    assert "PatientSuccessResponse" in definitions
    assert "PatientListSuccessResponse" in definitions
