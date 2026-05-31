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
    assert "/api/visits" in paths
    assert "/api/visits/{visit_id}" in paths
    assert "/api/patients/{patient_id}/visits" in paths
    assert "/api/aide-notes" in paths
    assert "/api/aide-notes/{aide_note_id}" in paths
    assert "/api/patients/{patient_id}/aide-notes" in paths
    assert "/api/visits/{visit_id}/aide-note" in paths
    assert "get" in paths["/api/health"]
    assert {"get", "post"} <= set(paths["/api/patients"].keys())
    assert {"get", "put", "delete"} <= set(
        paths["/api/patients/{patient_id}"].keys()
    )
    assert {"get", "post"} <= set(paths["/api/visits"].keys())
    assert {"get", "put", "delete"} <= set(paths["/api/visits/{visit_id}"].keys())
    assert "get" in paths["/api/patients/{patient_id}/visits"]
    assert {"get", "post"} <= set(paths["/api/aide-notes"].keys())
    assert {"get", "put", "delete"} <= set(
        paths["/api/aide-notes/{aide_note_id}"].keys()
    )
    assert "get" in paths["/api/patients/{patient_id}/aide-notes"]
    assert "get" in paths["/api/visits/{visit_id}/aide-note"]


def test_openapi_json_includes_patient_schemas(client):
    response = client.get("/api/openapi.json")
    definitions = response.get_json()["definitions"]

    assert "Patient" in definitions
    assert "PatientCreate" in definitions
    assert "PatientUpdate" in definitions
    assert "ErrorResponse" in definitions
    assert "PatientSuccessResponse" in definitions
    assert "PatientListSuccessResponse" in definitions
    assert "Visit" in definitions
    assert "VisitCreate" in definitions
    assert "VisitUpdate" in definitions
    assert "VisitResponse" in definitions
    assert "VisitListResponse" in definitions
    assert "AideNote" in definitions
    assert "AideNoteCreate" in definitions
    assert "AideNoteUpdate" in definitions
    assert "AideNoteResponse" in definitions
    assert "AideNoteListResponse" in definitions
