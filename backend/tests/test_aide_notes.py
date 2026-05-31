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
    }
    payload.update(overrides)
    return payload


def create_visit(client, patient_id, **overrides):
    return client.post("/api/visits", json=visit_payload(patient_id, **overrides)).get_json()[
        "data"
    ]


def aide_note_payload(patient_id, visit_id, **overrides):
    payload = {
        "patient_id": patient_id,
        "visit_id": visit_id,
        "personal_care": {"completed": ["bath", "oral_care"]},
        "nutrition": {"meal_percentage": 75, "fluids_offered": True},
        "mental_status": {"observed": ["alert", "oriented"]},
        "elimination": {"voided": True},
        "activity": {"ambulated": True},
        "assistive_devices": {"walker": True},
        "housekeeping": {"completed": ["laundry"]},
        "additional_notes": "Patient tolerated care well.",
        "aide_name": "Alex Morgan",
        "signature_data": "data:image/png;base64,placeholder",
        "signature_date": "2026-06-01",
        "time_in": "09:00",
        "time_out": "10:30",
    }
    payload.update(overrides)
    return payload


def create_aide_note(client, patient_id, visit_id, **overrides):
    return client.post(
        "/api/aide-notes",
        json=aide_note_payload(patient_id, visit_id, **overrides),
    )


def test_create_aide_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])

    response = create_aide_note(client, patient["id"], visit["id"])
    body = response.get_json()

    assert response.status_code == 201
    assert body["message"] == "Aide note created successfully"
    assert body["data"]["patient_id"] == patient["id"]
    assert body["data"]["visit_id"] == visit["id"]
    assert body["data"]["aide_name"] == "Alex Morgan"
    assert body["data"]["nutrition"]["meal_percentage"] == 75


def test_list_aide_notes(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    create_aide_note(client, patient["id"], visit["id"])

    response = client.get("/api/aide-notes")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Aide notes retrieved successfully"
    assert len(body["data"]) == 1


def test_get_aide_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_aide_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.get(f"/api/aide-notes/{created['id']}")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["id"] == created["id"]
    assert body["data"]["personal_care"]["completed"] == ["bath", "oral_care"]


def test_update_aide_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_aide_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.put(
        f"/api/aide-notes/{created['id']}",
        json={
            "aide_name": "Taylor Reed",
            "additional_notes": "Updated after supervisor review.",
        },
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Aide note updated successfully"
    assert body["data"]["aide_name"] == "Taylor Reed"


def test_delete_aide_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_aide_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.delete(f"/api/aide-notes/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Aide note deleted successfully"
    assert client.get(f"/api/aide-notes/{created['id']}").status_code == 404


def test_list_aide_notes_for_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    visit = create_visit(client, patient["id"])
    other_visit = create_visit(client, other_patient["id"])
    create_aide_note(client, patient["id"], visit["id"])
    create_aide_note(client, other_patient["id"], other_visit["id"])

    response = client.get(f"/api/patients/{patient['id']}/aide-notes")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Patient aide notes retrieved successfully"
    assert len(body["data"]) == 1
    assert body["data"][0]["patient_id"] == patient["id"]


def test_get_aide_note_by_visit(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_aide_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.get(f"/api/visits/{visit['id']}/aide-note")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Visit aide note retrieved successfully"
    assert body["data"]["id"] == created["id"]


def test_create_aide_note_requires_patient_id(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    payload = aide_note_payload(patient["id"], visit["id"])
    payload["patient_id"] = None

    response = client.post(
        "/api/aide-notes",
        json=payload,
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["patient_id"] == "This field is required."


def test_create_aide_note_requires_visit_id(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    payload = aide_note_payload(patient["id"], visit["id"])
    payload["visit_id"] = None

    response = client.post(
        "/api/aide-notes",
        json=payload,
    )

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == "This field is required."


def test_create_aide_note_requires_aide_name(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])

    response = create_aide_note(client, patient["id"], visit["id"], aide_name="")

    assert response.status_code == 400
    assert response.get_json()["errors"]["aide_name"] == "This field is required."


def test_create_aide_note_rejects_visit_for_different_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    visit = create_visit(client, other_patient["id"])

    response = create_aide_note(client, patient["id"], visit["id"])

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == (
        "Visit does not belong to the selected patient."
    )


def test_create_aide_note_rejects_duplicate_visit_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    create_aide_note(client, patient["id"], visit["id"])

    response = create_aide_note(client, patient["id"], visit["id"])

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == (
        "An aide note already exists for this visit."
    )
