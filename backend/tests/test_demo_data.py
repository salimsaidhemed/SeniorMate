from app.extensions import db
from app.models import (
    AideNote,
    MedicalRecord,
    NurseNote,
    Patient,
    PatientAssessment,
    Visit,
)


def demo_counts():
    return {
        "patients": Patient.query.filter_by(is_demo_data=True).count(),
        "visits": Visit.query.filter_by(is_demo_data=True).count(),
        "aide_notes": AideNote.query.filter_by(is_demo_data=True).count(),
        "nurse_notes": NurseNote.query.filter_by(is_demo_data=True).count(),
        "assessments": PatientAssessment.query.filter_by(is_demo_data=True).count(),
        "medical_records": MedicalRecord.query.filter_by(is_demo_data=True).count(),
    }


def test_seed_demo_refuses_when_disabled(app):
    result = app.test_cli_runner().invoke(args=["seed-demo"])

    assert result.exit_code == 1
    assert "DEMO_DATA_ENABLED=true" in result.output
    assert Patient.query.count() == 0


def test_seed_demo_refuses_in_production(app):
    app.config["DEMO_DATA_ENABLED"] = True
    app.config["APP_ENV"] = "production"

    result = app.test_cli_runner().invoke(args=["seed-demo"])

    assert result.exit_code == 1
    assert "APP_ENV=production" in result.output
    assert Patient.query.count() == 0


def test_seed_demo_creates_expected_records(app, medical_record_storage):
    app.config["DEMO_DATA_ENABLED"] = True

    result = app.test_cli_runner().invoke(args=["seed-demo"])

    assert result.exit_code == 0
    assert demo_counts() == {
        "patients": 24,
        "visits": 96,
        "aide_notes": 40,
        "nurse_notes": 40,
        "assessments": 48,
        "medical_records": 24,
    }
    assert len(medical_record_storage.objects) == 24
    assert "Demo data seeded" in result.output


def test_seed_demo_is_repeatable(app, medical_record_storage):
    app.config["DEMO_DATA_ENABLED"] = True
    runner = app.test_cli_runner()

    first = runner.invoke(args=["seed-demo"])
    second = runner.invoke(args=["seed-demo"])

    assert first.exit_code == 0
    assert second.exit_code == 0
    assert demo_counts()["patients"] == 24
    assert demo_counts()["visits"] == 96
    assert demo_counts()["medical_records"] == 24
    assert len(medical_record_storage.objects) == 24


def test_clear_demo_deletes_only_marked_records(app, medical_record_storage):
    app.config["DEMO_DATA_ENABLED"] = True
    runner = app.test_cli_runner()
    real_patient = Patient(
        first_name="Real",
        last_name="Patient",
        status="active",
        is_demo_data=False,
    )
    db.session.add(real_patient)
    db.session.commit()

    seeded = runner.invoke(args=["seed-demo"])
    cleared = runner.invoke(args=["clear-demo"])

    assert seeded.exit_code == 0
    assert cleared.exit_code == 0
    assert demo_counts() == {
        "patients": 0,
        "visits": 0,
        "aide_notes": 0,
        "nurse_notes": 0,
        "assessments": 0,
        "medical_records": 0,
    }
    assert db.session.get(Patient, real_patient.id) is not None
    assert Patient.query.filter_by(is_demo_data=False).count() == 1
    assert medical_record_storage.objects == {}
    assert "Demo data cleared" in cleared.output
