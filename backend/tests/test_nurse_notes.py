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
        "visit_type": "Skilled nursing visit",
        "staff_name": "Jordan Lee",
        "staff_role": "nurse",
    }
    payload.update(overrides)
    return payload


def create_visit(client, patient_id, **overrides):
    return client.post("/api/visits", json=visit_payload(patient_id, **overrides)).get_json()[
        "data"
    ]


def nurse_note_payload(patient_id, visit_id, **overrides):
    payload = {
        "patient_id": patient_id,
        "visit_id": visit_id,
        "diagnosis": "Hypertension",
        "living_arrangements": {"status": "lives with caregiver"},
        "visit_type": {"type": "routine skilled nursing"},
        "vital_signs": {"blood_pressure": "120/80", "pulse": 72},
        "diet": {"ordered": "low sodium"},
        "pain_assessment": {"pain_level": 2},
        "sensory": {"vision": "glasses"},
        "neuro": {"orientation": "oriented x3"},
        "respiratory": {"lungs": "clear"},
        "cardiac": {"rhythm": "regular"},
        "peripheral_circulation": {"edema": "none"},
        "genitourinary": {"voiding": "normal"},
        "gastrointestinal": {"bowel_sounds": "present"},
        "endocrine": {"blood_glucose": 110},
        "skin_integrity": {"intact": True},
        "wound_evaluation": {"wounds": []},
        "mental_status": {"mood": "calm"},
        "functional_status": {"ambulation": "walker"},
        "homebound_status": {"reason": "requires assistance to leave home"},
        "skilled_nursing": "Medication reconciliation completed.",
        "response_to_intervention": "Patient verbalized understanding.",
        "patient_caregiver_understanding": {"understood": True},
        "md_contact": {"contacted": False},
        "discharge_planning": "Continue plan of care.",
        "patient_feedback": "Patient reports feeling stable.",
        "narrative": "Skilled nursing visit completed without incident.",
        "signature_data": "data:image/png;base64,placeholder",
        "signature_date": "2026-06-01",
    }
    payload.update(overrides)
    return payload


def create_nurse_note(client, patient_id, visit_id, **overrides):
    return client.post(
        "/api/nurse-notes",
        json=nurse_note_payload(patient_id, visit_id, **overrides),
    )


def test_create_nurse_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])

    response = create_nurse_note(client, patient["id"], visit["id"])
    body = response.get_json()

    assert response.status_code == 201
    assert body["message"] == "Nurse note created successfully"
    assert body["data"]["patient_id"] == patient["id"]
    assert body["data"]["visit_id"] == visit["id"]
    assert body["data"]["diagnosis"] == "Hypertension"
    assert body["data"]["vital_signs"]["blood_pressure"] == "120/80"


def test_list_nurse_notes(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    create_nurse_note(client, patient["id"], visit["id"])

    response = client.get("/api/nurse-notes")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Nurse notes retrieved successfully"
    assert len(body["data"]) == 1


def test_get_nurse_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_nurse_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.get(f"/api/nurse-notes/{created['id']}")
    body = response.get_json()

    assert response.status_code == 200
    assert body["data"]["id"] == created["id"]
    assert body["data"]["diagnosis"] == "Hypertension"


def test_update_nurse_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_nurse_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.put(
        f"/api/nurse-notes/{created['id']}",
        json={
            "diagnosis": "Hypertension and diabetes",
            "narrative": "Updated after nursing review.",
        },
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Nurse note updated successfully"
    assert body["data"]["diagnosis"] == "Hypertension and diabetes"


def test_delete_nurse_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_nurse_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.delete(f"/api/nurse-notes/{created['id']}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Nurse note deleted successfully"
    assert client.get(f"/api/nurse-notes/{created['id']}").status_code == 404


def test_list_nurse_notes_for_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    visit = create_visit(client, patient["id"])
    other_visit = create_visit(client, other_patient["id"])
    create_nurse_note(client, patient["id"], visit["id"])
    create_nurse_note(client, other_patient["id"], other_visit["id"])

    response = client.get(f"/api/patients/{patient['id']}/nurse-notes")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Patient nurse notes retrieved successfully"
    assert len(body["data"]) == 1
    assert body["data"][0]["patient_id"] == patient["id"]


def test_get_nurse_note_by_visit(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    created = create_nurse_note(client, patient["id"], visit["id"]).get_json()["data"]

    response = client.get(f"/api/visits/{visit['id']}/nurse-note")
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Visit nurse note retrieved successfully"
    assert body["data"]["id"] == created["id"]


def test_create_nurse_note_requires_patient_id(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    payload = nurse_note_payload(patient["id"], visit["id"])
    payload["patient_id"] = None

    response = client.post("/api/nurse-notes", json=payload)

    assert response.status_code == 400
    assert response.get_json()["errors"]["patient_id"] == "This field is required."


def test_create_nurse_note_requires_visit_id(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    payload = nurse_note_payload(patient["id"], visit["id"])
    payload["visit_id"] = None

    response = client.post("/api/nurse-notes", json=payload)

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == "This field is required."


def test_create_nurse_note_rejects_visit_for_different_patient(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    visit = create_visit(client, other_patient["id"])

    response = create_nurse_note(client, patient["id"], visit["id"])

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == (
        "Visit does not belong to the selected patient."
    )


def test_create_nurse_note_rejects_duplicate_visit_note(client):
    patient = create_patient(client)
    visit = create_visit(client, patient["id"])
    create_nurse_note(client, patient["id"], visit["id"])

    response = create_nurse_note(client, patient["id"], visit["id"])

    assert response.status_code == 400
    assert response.get_json()["errors"]["visit_id"] == (
        "A nurse note already exists for this visit."
    )
