def patient_payload(**overrides):
    payload = {
        "first_name": "Maria",
        "last_name": "Santos",
        "date_of_birth": "1945-03-12",
        "gender": "female",
        "phone": "+1-555-0100",
        "email": "maria.santos@example.com",
        "address": "12 Care Lane",
        "emergency_contact_name": "Ana Santos",
        "emergency_contact_phone": "+1-555-0199",
        "diagnosis_summary": "Requires daily mobility support.",
    }
    payload.update(overrides)
    return payload


def create_patient(client, **overrides):
    return client.post("/api/patients", json=patient_payload(**overrides))


def test_create_patient(client):
    response = create_patient(client)
    body = response.get_json()

    assert response.status_code == 201
    assert body["message"] == "Patient created successfully"
    assert body["data"]["id"] is not None
    assert body["data"]["first_name"] == "Maria"
    assert body["data"]["status"] == "active"


def test_list_patients(client):
    create_patient(client)
    create_patient(client, first_name="John", last_name="Rivera")

    response = client.get("/api/patients")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Patients retrieved successfully"
    assert len(body["data"]) == 2


def test_get_patient(client):
    created = create_patient(client).get_json()["data"]

    response = client.get(f"/api/patients/{created['id']}")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["id"] == created["id"]
    assert body["data"]["last_name"] == "Santos"


def test_update_patient(client):
    created = create_patient(client).get_json()["data"]

    response = client.put(
        f"/api/patients/{created['id']}",
        json={"phone": "+1-555-0111", "status": "inactive"},
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Patient updated successfully"
    assert body["data"]["phone"] == "+1-555-0111"
    assert body["data"]["status"] == "inactive"


def test_delete_patient(client):
    created = create_patient(client).get_json()["data"]

    response = client.delete(f"/api/patients/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Patient deleted successfully"
    assert client.get(f"/api/patients/{created['id']}").status_code == 404


def test_create_patient_requires_first_and_last_name(client):
    response = client.post("/api/patients", json={"first_name": ""})
    body = response.get_json()

    assert response.status_code == 400
    assert body["message"] == "Invalid patient data"
    assert body["errors"]["first_name"] == "This field is required."
    assert body["errors"]["last_name"] == "This field is required."


def test_create_patient_validates_date_of_birth(client):
    response = client.post(
        "/api/patients",
        json=patient_payload(date_of_birth="12-03-1945"),
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["date_of_birth"] == (
        "Use ISO date format YYYY-MM-DD."
    )
