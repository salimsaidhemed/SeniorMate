from datetime import date

import pytest

from app.demo_data import seed_demo_records
from app.models import Patient
from tests.test_auth import enable_auth, token_claims


REPORT_PATHS = (
    "/api/reports/patient-census",
    "/api/reports/visit-activity",
    "/api/reports/staff-activity",
    "/api/reports/assessment-summary",
    "/api/reports/medical-records-summary",
)


@pytest.fixture()
def seeded_reports(app):
    app.config["DEMO_DATA_ENABLED"] = True
    with app.app_context():
        counts = seed_demo_records(today=date(2026, 6, 11))
    return counts


@pytest.mark.parametrize("path", REPORT_PATHS)
def test_reports_return_safe_empty_structure(client, path):
    response = client.get(path)
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert set(data) == {"summary", "groups", "recent", "rows"}
    assert data["rows"] == []
    assert data["recent"] == []


def test_patient_census_report_structure(client, seeded_reports):
    response = client.get("/api/reports/patient-census")
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["summary"] == {
        "total_patients": 24,
        "active_patients": 21,
        "inactive_patients": 3,
    }
    assert len(data["rows"]) == 24
    assert data["groups"]["patients_by_gender"]
    assert data["groups"]["patients_by_diagnosis"]


def test_visit_activity_report_filters_dates_and_status(client, seeded_reports):
    response = client.get(
        "/api/reports/visit-activity",
        query_string={
            "start_date": "2026-06-01",
            "end_date": "2026-06-11",
            "status": "completed",
        },
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["summary"]["total_visits"] > 0
    assert all(row["status"] == "completed" for row in data["rows"])
    assert all(
        date.fromisoformat(row["visit_date"])
        >= date(2026, 6, 1)
        for row in data["rows"]
    )


def test_staff_activity_report_counts_linked_work(client, seeded_reports):
    response = client.get(
        "/api/reports/staff-activity",
        query_string={"staff_role": "aide"},
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["summary"]["total_staff"] == 2
    assert data["summary"]["total_visits"] == 48
    assert data["summary"]["total_notes"] == 40
    assert all(row["staff_role"] == "aide" for row in data["rows"])


def test_assessment_summary_report_filters_patient(client, seeded_reports):
    patient = Patient.query.filter_by(is_demo_data=True).first()
    response = client.get(
        "/api/reports/assessment-summary",
        query_string={"patient_id": patient.id, "status": "completed"},
    )
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["summary"]["total_assessments"] == 1
    assert data["summary"]["linked_to_visits"] == 1
    assert all(row["status"] == "completed" for row in data["rows"])


def test_medical_records_summary_report_structure(client, seeded_reports):
    response = client.get("/api/reports/medical-records-summary")
    data = response.get_json()["data"]

    assert response.status_code == 200
    assert data["summary"]["total_records"] == 24
    assert data["summary"]["patients_with_records"] == 24
    assert data["groups"]["records_by_type"] == [
        {"label": "care_plan", "count": 24}
    ]


@pytest.mark.parametrize("path", REPORT_PATHS)
def test_report_csv_export(client, seeded_reports, path):
    response = client.get(path, query_string={"format": "csv"})

    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "attachment;" in response.headers["Content-Disposition"]
    assert len(response.get_data(as_text=True).splitlines()) > 1


def test_invalid_report_date_returns_clear_error(client):
    response = client.get(
        "/api/reports/visit-activity",
        query_string={"start_date": "not-a-date"},
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == (
        "start_date must use YYYY-MM-DD format."
    )


def test_reports_require_authentication_when_enabled(app, client):
    app.config["AUTH_ENABLED"] = True

    response = client.get("/api/reports/patient-census")

    assert response.status_code == 401


def test_viewer_can_access_reports(app, client, monkeypatch):
    enable_auth(app, monkeypatch, token_claims("viewer"))

    response = client.get(
        "/api/reports/patient-census",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 200


def test_unknown_role_cannot_access_reports(app, client, monkeypatch):
    enable_auth(app, monkeypatch, token_claims("unrecognized"))

    response = client.get(
        "/api/reports/patient-census",
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 403
