from datetime import UTC, date, datetime


def current_month_date(day=1):
    today = datetime.now(UTC).date()
    return date(today.year, today.month, day).isoformat()


def prior_month_date():
    today = datetime.now(UTC).date()

    if today.month == 1:
        return date(today.year - 1, 12, 15).isoformat()

    return date(today.year, today.month - 1, 15).isoformat()


def patient_payload(**overrides):
    payload = {
        "first_name": "Maria",
        "last_name": "Santos",
        "gender": "female",
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
        "visit_date": current_month_date(),
        "visit_type": "Skilled nursing visit",
        "staff_name": "Jordan Lee",
        "staff_role": "nurse",
        "status": "completed",
    }
    payload.update(overrides)
    return payload


def create_visit(client, patient_id, **overrides):
    return client.post("/api/visits", json=visit_payload(patient_id, **overrides)).get_json()[
        "data"
    ]


def create_aide_note(client, patient_id, visit_id):
    return client.post(
        "/api/aide-notes",
        json={
            "patient_id": patient_id,
            "visit_id": visit_id,
            "aide_name": "Alex Morgan",
            "time_in": "09:00",
            "time_out": "10:00",
        },
    ).get_json()["data"]


def create_nurse_note(client, patient_id, visit_id):
    return client.post(
        "/api/nurse-notes",
        json={
            "patient_id": patient_id,
            "visit_id": visit_id,
            "diagnosis": "Hypertension",
        },
    ).get_json()["data"]


def test_dashboard_stats_endpoint_returns_expected_keys(client):
    response = client.get("/api/dashboard/stats")
    body = response.get_json()

    expected_keys = {
        "total_patients",
        "active_patients",
        "inactive_patients",
        "total_visits",
        "visits_this_month",
        "aide_notes_this_month",
        "nurse_notes_this_month",
        "patients_by_status",
        "patients_by_gender",
        "visits_by_type",
        "visits_by_status",
        "recent_visits",
    }

    assert response.status_code == 200
    assert body["message"] == "Dashboard stats retrieved successfully"
    assert expected_keys <= set(body["data"].keys())


def test_dashboard_stats_counts_are_correct(client):
    active_patient = create_patient(client)
    inactive_patient = create_patient(
        client,
        first_name="John",
        last_name="Rivera",
        gender="male",
        status="inactive",
    )

    current_visit = create_visit(client, active_patient["id"])
    create_visit(
        client,
        inactive_patient["id"],
        visit_date=prior_month_date(),
        visit_type="Home health aide visit",
        staff_role="aide",
        status="scheduled",
    )
    aide_visit = create_visit(
        client,
        active_patient["id"],
        visit_date=current_month_date(2),
        visit_type="Home health aide visit",
        staff_role="aide",
    )
    nurse_visit = create_visit(
        client,
        active_patient["id"],
        visit_date=current_month_date(3),
    )
    create_aide_note(client, active_patient["id"], aide_visit["id"])
    create_nurse_note(client, active_patient["id"], nurse_visit["id"])

    response = client.get("/api/dashboard/stats")
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["total_patients"] == 2
    assert data["active_patients"] == 1
    assert data["inactive_patients"] == 1
    assert data["total_visits"] == 4
    assert data["visits_this_month"] == 3
    assert data["aide_notes_this_month"] == 1
    assert data["nurse_notes_this_month"] == 1
    assert {"label": "active", "count": 1} in data["patients_by_status"]
    assert {"label": "inactive", "count": 1} in data["patients_by_status"]
    assert {"label": "female", "count": 1} in data["patients_by_gender"]
    assert {"label": "male", "count": 1} in data["patients_by_gender"]
    assert {"label": "Skilled nursing visit", "count": 2} in data["visits_by_type"]
    assert {"label": "completed", "count": 3} in data["visits_by_status"]
    assert data["recent_visits"][0]["id"] == nurse_visit["id"]
    assert data["recent_visits"][0]["patient_name"] == "Maria Santos"
    assert current_visit["id"] in [visit["id"] for visit in data["recent_visits"]]


def test_dashboard_recent_visits_are_returned_in_expected_order(client):
    patient = create_patient(client)
    first = create_visit(client, patient["id"], visit_date=current_month_date(1))
    second = create_visit(client, patient["id"], visit_date=current_month_date(2))
    third = create_visit(client, patient["id"], visit_date=current_month_date(3))

    response = client.get("/api/dashboard/stats")
    recent_ids = [visit["id"] for visit in response.get_json()["data"]["recent_visits"]]

    assert response.status_code == 200
    assert recent_ids[:3] == [third["id"], second["id"], first["id"]]
