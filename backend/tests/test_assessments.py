def create_patient(client, first_name="Maria", last_name="Santos"):
    return client.post(
        "/api/patients",
        json={"first_name": first_name, "last_name": last_name},
    ).get_json()["data"]


def create_visit(client, patient_id):
    return client.post(
        "/api/visits",
        json={
            "patient_id": patient_id,
            "visit_date": "2026-06-10",
            "visit_type": "Skilled nursing visit",
            "staff_role": "nurse",
        },
    ).get_json()["data"]


def assessment_payload(patient_id, **overrides):
    payload = {
        "patient_id": patient_id,
        "assessment_type": "fall_risk",
        "assessment_date": "2026-06-10",
        "performed_by": "Jordan Lee, RN",
        "summary": "Moderate fall risk identified.",
        "findings": {
            "risk_level": "moderate",
            "observations": ["Uses walker"],
        },
        "recommendations": "Continue walker use.",
        "status": "completed",
    }
    payload.update(overrides)
    return payload


def create_assessment(client, patient_id, **overrides):
    return client.post(
        "/api/assessments",
        json=assessment_payload(patient_id, **overrides),
    )


def test_create_assessment(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])

    response = create_assessment(client, patient["id"], visit_id=visit["id"])
    body = response.get_json()

    assert response.status_code == 201
    assert body["message"] == "Assessment created successfully"
    assert body["data"]["patient_id"] == patient["id"]
    assert body["data"]["visit_id"] == visit["id"]
    assert body["data"]["assessment_type"] == "fall_risk"
    assert body["data"]["findings"]["risk_level"] == "moderate"


def test_list_assessments(client):
    patient = create_patient(client)
    create_assessment(client, patient["id"])

    response = client.get("/api/assessments")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Assessments retrieved successfully"
    assert len(response.get_json()["data"]) == 1


def test_get_assessment(client):
    patient = create_patient(client)
    created = create_assessment(client, patient["id"]).get_json()["data"]

    response = client.get(f"/api/assessments/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["data"]["id"] == created["id"]


def test_update_assessment(client):
    patient = create_patient(client)
    created = create_assessment(client, patient["id"]).get_json()["data"]

    response = client.put(
        f"/api/assessments/{created['id']}",
        json={
            "assessment_type": "mobility",
            "summary": "Mobility improved with supervision.",
            "status": "draft",
        },
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Assessment updated successfully"
    assert body["data"]["assessment_type"] == "mobility"
    assert body["data"]["status"] == "draft"


def test_delete_assessment(client):
    patient = create_patient(client)
    created = create_assessment(client, patient["id"]).get_json()["data"]

    response = client.delete(f"/api/assessments/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Assessment deleted successfully"
    assert client.get(f"/api/assessments/{created['id']}").status_code == 404


def test_list_assessments_for_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, "John", "Rivera")
    create_assessment(client, patient["id"])
    create_assessment(client, other_patient["id"], assessment_type="nutrition")

    response = client.get(f"/api/patients/{patient['id']}/assessments")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Patient assessments retrieved successfully"
    assert len(body["data"]) == 1
    assert body["data"][0]["patient_id"] == patient["id"]


def test_list_assessments_for_visit(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    other_visit = create_visit(client, patient["id"])
    create_assessment(client, patient["id"], visit_id=visit["id"])
    create_assessment(
        client,
        patient["id"],
        visit_id=other_visit["id"],
        assessment_type="general",
    )

    response = client.get(f"/api/visits/{visit['id']}/assessments")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Visit assessments retrieved successfully"
    assert len(body["data"]) == 1
    assert body["data"][0]["visit_id"] == visit["id"]


def test_create_assessment_rejects_invalid_patient(client):
    response = create_assessment(client, 999)

    assert response.status_code == 400
    assert response.get_json()["errors"]["patient_id"] == "Patient not found."


def test_create_assessment_rejects_invalid_visit(client):
    patient = create_patient(client)

    response = create_assessment(client, patient["id"], visit_id=999)

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == "Visit not found."


def test_create_assessment_rejects_visit_for_different_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, "John", "Rivera")
    visit = create_visit(client, other_patient["id"])

    response = create_assessment(client, patient["id"], visit_id=visit["id"])

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == (
        "Visit does not belong to the selected patient."
    )


def test_create_assessment_requires_core_fields(client):
    response = client.post("/api/assessments", json={})
    errors = response.get_json()["errors"]

    assert response.status_code == 400
    assert errors["patient_id"] == "This field is required."
    assert errors["assessment_type"] == "This field is required."
    assert errors["assessment_date"] == "This field is required."


def test_assessment_defaults_to_draft(client):
    patient = create_patient(client)
    payload = assessment_payload(patient["id"])
    payload.pop("status")

    response = client.post("/api/assessments", json=payload)

    assert response.status_code == 201
    assert response.get_json()["data"]["status"] == "draft"
