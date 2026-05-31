def patient_payload(**overrides):
    payload = {
        "first_name": "Maria",
        "last_name": "Santos",
        "date_of_birth": "1945-03-12",
    }
    payload.update(overrides)
    return payload


def create_patient(client, **overrides):
    return client.post("/api/patients", json=patient_payload(**overrides)).get_json()[
        "data"
    ]


def visit_payload(patient_id, **overrides):
    payload = {
        "patient_id": patient_id,
        "visit_date": "2026-06-01",
        "visit_type": "Home care visit",
        "staff_name": "Jordan Lee",
        "staff_role": "aide",
        "time_in": "09:00",
        "time_out": "10:30",
        "notes": "Patient completed morning mobility exercises.",
    }
    payload.update(overrides)
    return payload


def create_visit(client, patient_id, **overrides):
    return client.post("/api/visits", json=visit_payload(patient_id, **overrides))


def test_create_visit_for_patient(client):
    patient = create_patient(client)

    response = create_visit(client, patient["id"])
    body = response.get_json()

    assert response.status_code == 201
    assert body["message"] == "Visit created successfully"
    assert body["data"]["patient_id"] == patient["id"]
    assert body["data"]["visit_date"] == "2026-06-01"
    assert body["data"]["visit_type"] == "Home care visit"
    assert body["data"]["status"] == "scheduled"


def test_list_visits(client):
    patient = create_patient(client)
    create_visit(client, patient["id"])
    create_visit(client, patient["id"], visit_date="2026-06-02", staff_role="nurse")

    response = client.get("/api/visits")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Visits retrieved successfully"
    assert len(body["data"]) == 2


def test_list_visits_for_specific_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    create_visit(client, patient["id"])
    create_visit(client, other_patient["id"])

    response = client.get(f"/api/patients/{patient['id']}/visits")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Patient visits retrieved successfully"
    assert len(body["data"]) == 1
    assert body["data"][0]["patient_id"] == patient["id"]


def test_get_visit(client):
    patient = create_patient(client)
    created = create_visit(client, patient["id"]).get_json()["data"]

    response = client.get(f"/api/visits/{created['id']}")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["id"] == created["id"]
    assert body["data"]["staff_name"] == "Jordan Lee"


def test_update_visit(client):
    patient = create_patient(client)
    created = create_visit(client, patient["id"]).get_json()["data"]

    response = client.put(
        f"/api/visits/{created['id']}",
        json={
            "staff_role": "nurse",
            "status": "completed",
            "notes": "Vitals checked and medication reminder completed.",
        },
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Visit updated successfully"
    assert body["data"]["staff_role"] == "nurse"
    assert body["data"]["status"] == "completed"


def test_delete_visit(client):
    patient = create_patient(client)
    created = create_visit(client, patient["id"]).get_json()["data"]

    response = client.delete(f"/api/visits/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Visit deleted successfully"
    assert client.get(f"/api/visits/{created['id']}").status_code == 404


def test_create_visit_requires_patient_id_and_visit_date(client):
    response = client.post("/api/visits", json={"visit_type": "Home care visit"})
    body = response.get_json()

    assert response.status_code == 400
    assert body["message"] == "Invalid visit data"
    assert body["errors"]["patient_id"] == "This field is required."
    assert body["errors"]["visit_date"] == "This field is required."


def test_create_visit_rejects_invalid_patient_id(client):
    response = client.post("/api/visits", json=visit_payload(999))
    body = response.get_json()

    assert response.status_code == 400
    assert body["message"] == "Invalid visit data"
    assert body["errors"]["patient_id"] == "Patient not found."


def test_create_visit_validates_staff_role(client):
    patient = create_patient(client)

    response = create_visit(client, patient["id"], staff_role="therapist")

    assert response.status_code == 400
    assert response.get_json()["errors"]["staff_role"] == (
        "Staff role must be aide or nurse."
    )
