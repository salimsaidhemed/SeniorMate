from datetime import UTC, datetime


def current_month_date(day=1):
    today = datetime.now(UTC).date()
    return today.replace(day=day).isoformat()


def patient_payload(**overrides):
    payload = {
        "first_name": "Maria",
        "last_name": "Santos",
        "gender": "female",
        "phone": "+1-555-0100",
        "email": "maria@example.com",
        "diagnosis_summary": "Diabetes care and mobility support.",
        "status": "active",
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
        "visit_date": current_month_date(1),
        "visit_type": "Skilled nursing visit",
        "staff_name": "Jordan Lee",
        "staff_role": "nurse",
        "status": "completed",
        "notes": "Medication review completed.",
    }
    payload.update(overrides)
    return payload


def create_visit(client, patient_id, **overrides):
    return client.post("/api/visits", json=visit_payload(patient_id, **overrides)).get_json()[
        "data"
    ]


def create_aide_note(client, patient_id, visit_id, **overrides):
    payload = {
        "patient_id": patient_id,
        "visit_id": visit_id,
        "aide_name": "Alex Morgan",
        "time_in": "09:00",
        "time_out": "10:00",
    }
    payload.update(overrides)
    return client.post("/api/aide-notes", json=payload).get_json()["data"]


def create_nurse_note(client, patient_id, visit_id, **overrides):
    payload = {
        "patient_id": patient_id,
        "visit_id": visit_id,
        "diagnosis": "Hypertension",
    }
    payload.update(overrides)
    return client.post("/api/nurse-notes", json=payload).get_json()["data"]


def test_patient_search_and_status_filter(client):
    create_patient(client)
    create_patient(
        client,
        first_name="John",
        last_name="Rivera",
        gender="male",
        email="john@example.com",
        diagnosis_summary="Cardiac monitoring.",
        status="inactive",
    )

    search_response = client.get("/api/patients?search=diabetes")
    status_response = client.get("/api/patients?status=inactive")

    assert search_response.status_code == 200
    assert [patient["first_name"] for patient in search_response.get_json()["data"]] == [
        "Maria"
    ]
    assert status_response.get_json()["pagination"]["total"] == 1
    assert status_response.get_json()["data"][0]["status"] == "inactive"


def test_patient_pagination_metadata(client):
    create_patient(client, first_name="Ana")
    create_patient(client, first_name="Ben")
    create_patient(client, first_name="Cara")

    response = client.get("/api/patients?page=2&per_page=2")
    body = response.get_json()

    assert response.status_code == 200
    assert body["pagination"] == {
        "page": 2,
        "per_page": 2,
        "total": 3,
        "pages": 2,
    }
    assert len(body["data"]) == 1


def test_visit_patient_filter_and_date_range(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    create_visit(client, patient["id"], visit_date="2026-06-01")
    create_visit(client, patient["id"], visit_date="2026-06-15")
    create_visit(client, other_patient["id"], visit_date="2026-06-20")

    patient_response = client.get(f"/api/visits?patient_id={patient['id']}")
    range_response = client.get("/api/visits?start_date=2026-06-10&end_date=2026-06-30")

    assert patient_response.status_code == 200
    assert patient_response.get_json()["pagination"]["total"] == 2
    assert range_response.get_json()["pagination"]["total"] == 2
    assert all(
        visit["visit_date"] >= "2026-06-10" for visit in range_response.get_json()["data"]
    )


def test_visit_search_by_patient_name_and_staff(client):
    patient = create_patient(client, first_name="Clara", last_name="Barton")
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    create_visit(client, patient["id"], staff_name="Nora Nurse")
    create_visit(client, other_patient["id"], staff_name="Alex Aide")

    patient_search = client.get("/api/visits?search=Clara")
    staff_search = client.get("/api/visits?search=Alex")

    assert patient_search.get_json()["pagination"]["total"] == 1
    assert patient_search.get_json()["data"][0]["patient_id"] == patient["id"]
    assert staff_search.get_json()["pagination"]["total"] == 1
    assert staff_search.get_json()["data"][0]["staff_name"] == "Alex Aide"


def test_aide_note_filtering(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    visit = create_visit(client, patient["id"])
    other_visit = create_visit(client, other_patient["id"])
    create_aide_note(client, patient["id"], visit["id"], aide_name="Alex Morgan")
    create_aide_note(client, other_patient["id"], other_visit["id"], aide_name="Taylor Reed")

    patient_response = client.get(f"/api/aide-notes?patient_id={patient['id']}")
    aide_response = client.get("/api/aide-notes?aide_name=Taylor")

    assert patient_response.status_code == 200
    assert patient_response.get_json()["pagination"]["total"] == 1
    assert aide_response.get_json()["data"][0]["aide_name"] == "Taylor Reed"


def test_nurse_note_filtering(client):
    patient = create_patient(client)
    other_patient = create_patient(client, first_name="John", last_name="Rivera")
    visit = create_visit(client, patient["id"])
    other_visit = create_visit(client, other_patient["id"])
    create_nurse_note(client, patient["id"], visit["id"], diagnosis="Hypertension")
    create_nurse_note(
        client,
        other_patient["id"],
        other_visit["id"],
        diagnosis="Diabetes monitoring",
    )

    patient_response = client.get(f"/api/nurse-notes?patient_id={patient['id']}")
    diagnosis_response = client.get("/api/nurse-notes?diagnosis=diabetes")

    assert patient_response.status_code == 200
    assert patient_response.get_json()["pagination"]["total"] == 1
    assert diagnosis_response.get_json()["data"][0]["diagnosis"] == "Diabetes monitoring"
