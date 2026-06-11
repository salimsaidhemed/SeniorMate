import csv
from collections import Counter, defaultdict
from datetime import UTC, datetime, time
from io import StringIO

from flasgger import swag_from
from flask import Blueprint, Response, jsonify, request

from app.models import (
    MedicalRecord,
    Patient,
    PatientAssessment,
    Visit,
)
from app.swagger import (
    assessment_summary_report_spec,
    medical_records_summary_report_spec,
    patient_census_report_spec,
    staff_activity_report_spec,
    visit_activity_report_spec,
)


reports_bp = Blueprint("reports", __name__, url_prefix="/api/reports")


def _parse_date(name):
    value = request.args.get(name)
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"{name} must use YYYY-MM-DD format.") from None


def _parse_patient_id():
    value = request.args.get("patient_id")
    if not value:
        return None
    try:
        patient_id = int(value)
    except ValueError:
        raise ValueError("patient_id must be a positive integer.") from None
    if patient_id < 1:
        raise ValueError("patient_id must be a positive integer.")
    return patient_id


def _filters():
    start_date = _parse_date("start_date")
    end_date = _parse_date("end_date")
    if start_date and end_date and start_date > end_date:
        raise ValueError("start_date must be on or before end_date.")
    return {
        "start_date": start_date,
        "end_date": end_date,
        "patient_id": _parse_patient_id(),
        "staff_role": request.args.get("staff_role"),
        "staff_name": request.args.get("staff_name"),
        "visit_type": request.args.get("visit_type"),
        "status": request.args.get("status"),
    }


def _group_counts(values, empty_label="Not specified"):
    counts = Counter(value or empty_label for value in values)
    return [
        {"label": label, "count": count}
        for label, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]


def _date_groups(values):
    return [
        {"label": label, "count": count}
        for label, count in sorted(Counter(values).items())
    ]


def _date_boundary(value, boundary):
    return datetime.combine(value, boundary, tzinfo=UTC)


def _patient_name(patient):
    return f"{patient.first_name} {patient.last_name}"


def _success(data, message):
    return jsonify({"data": data, "message": message})


def _csv_response(name, headers, rows):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{name}.csv"'},
    )


def _respond(name, data, headers):
    if request.args.get("format", "json").lower() == "csv":
        return _csv_response(name, headers, data["rows"])
    return _success(data, f"{name.replace('-', ' ').title()} retrieved successfully")


def _apply_visit_filters(query, filters):
    if filters["start_date"]:
        query = query.filter(Visit.visit_date >= filters["start_date"])
    if filters["end_date"]:
        query = query.filter(Visit.visit_date <= filters["end_date"])
    if filters["patient_id"]:
        query = query.filter(Visit.patient_id == filters["patient_id"])
    if filters["staff_role"]:
        query = query.filter(Visit.staff_role == filters["staff_role"])
    if filters["staff_name"]:
        query = query.filter(Visit.staff_name.ilike(f"%{filters['staff_name']}%"))
    if filters["visit_type"]:
        query = query.filter(Visit.visit_type == filters["visit_type"])
    if filters["status"]:
        query = query.filter(Visit.status == filters["status"])
    return query


def _report_errors(view):
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except ValueError as exc:
            return jsonify({"message": str(exc)}), 400

    wrapped.__name__ = view.__name__
    return wrapped


@reports_bp.get("/patient-census")
@swag_from(patient_census_report_spec)
@_report_errors
def patient_census_report():
    filters = _filters()
    query = Patient.query
    if filters["patient_id"]:
        query = query.filter(Patient.id == filters["patient_id"])
    if filters["status"]:
        query = query.filter(Patient.status == filters["status"])
    if filters["start_date"]:
        query = query.filter(
            Patient.created_at >= _date_boundary(filters["start_date"], time.min)
        )
    if filters["end_date"]:
        query = query.filter(
            Patient.created_at <= _date_boundary(filters["end_date"], time.max)
        )
    patients = query.order_by(Patient.created_at.desc(), Patient.id.desc()).all()
    rows = [
        {
            "patient_id": patient.id,
            "patient_name": _patient_name(patient),
            "status": patient.status,
            "gender": patient.gender or "",
            "date_of_birth": patient.date_of_birth.isoformat()
            if patient.date_of_birth
            else "",
            "diagnosis": patient.diagnosis_summary or "",
            "created_at": patient.created_at.date().isoformat(),
        }
        for patient in patients
    ]
    data = {
        "summary": {
            "total_patients": len(patients),
            "active_patients": sum(p.status == "active" for p in patients),
            "inactive_patients": sum(p.status == "inactive" for p in patients),
        },
        "groups": {
            "patients_by_gender": _group_counts(p.gender for p in patients),
            "patients_by_diagnosis": _group_counts(
                p.diagnosis_summary for p in patients
            ),
        },
        "recent": rows[:10],
        "rows": rows,
    }
    return _respond(
        "patient-census",
        data,
        [
            "patient_id",
            "patient_name",
            "status",
            "gender",
            "date_of_birth",
            "diagnosis",
            "created_at",
        ],
    )


@reports_bp.get("/visit-activity")
@swag_from(visit_activity_report_spec)
@_report_errors
def visit_activity_report():
    filters = _filters()
    visits = (
        _apply_visit_filters(Visit.query, filters)
        .order_by(Visit.visit_date.desc(), Visit.id.desc())
        .all()
    )
    rows = [
        {
            "visit_id": visit.id,
            "patient_name": _patient_name(visit.patient),
            "visit_date": visit.visit_date.isoformat(),
            "visit_type": visit.visit_type,
            "staff_name": visit.staff_name or "",
            "staff_role": visit.staff_role or "",
            "status": visit.status,
        }
        for visit in visits
    ]
    data = {
        "summary": {
            "total_visits": len(visits),
            "completed_visits": sum(v.status == "completed" for v in visits),
            "scheduled_visits": sum(v.status == "scheduled" for v in visits),
            "cancelled_visits": sum(v.status == "cancelled" for v in visits),
        },
        "groups": {
            "visits_by_type": _group_counts(v.visit_type for v in visits),
            "visits_by_status": _group_counts(v.status for v in visits),
            "visits_by_staff_role": _group_counts(v.staff_role for v in visits),
            "visits_over_time": _date_groups(
                v.visit_date.isoformat() for v in visits
            ),
        },
        "recent": rows[:10],
        "rows": rows,
    }
    return _respond(
        "visit-activity",
        data,
        [
            "visit_id",
            "patient_name",
            "visit_date",
            "visit_type",
            "staff_name",
            "staff_role",
            "status",
        ],
    )


@reports_bp.get("/staff-activity")
@swag_from(staff_activity_report_spec)
@_report_errors
def staff_activity_report():
    filters = _filters()
    visits = _apply_visit_filters(Visit.query, filters).all()
    staff = defaultdict(
        lambda: {
            "staff_name": "",
            "staff_role": "",
            "total_visits": 0,
            "aide_notes_completed": 0,
            "nurse_notes_completed": 0,
            "assessments_completed": 0,
        }
    )
    visit_ids = {visit.id for visit in visits}
    for visit in visits:
        key = (visit.staff_name or "Unassigned", visit.staff_role or "unspecified")
        staff[key]["staff_name"], staff[key]["staff_role"] = key
        staff[key]["total_visits"] += 1
        if visit.aide_note:
            staff[key]["aide_notes_completed"] += 1
        if visit.nurse_note:
            staff[key]["nurse_notes_completed"] += 1

    assessment_query = PatientAssessment.query.filter(
        PatientAssessment.status == "completed"
    )
    if filters["start_date"]:
        assessment_query = assessment_query.filter(
            PatientAssessment.assessment_date >= filters["start_date"]
        )
    if filters["end_date"]:
        assessment_query = assessment_query.filter(
            PatientAssessment.assessment_date <= filters["end_date"]
        )
    if filters["patient_id"]:
        assessment_query = assessment_query.filter(
            PatientAssessment.patient_id == filters["patient_id"]
        )
    if filters["staff_name"]:
        assessment_query = assessment_query.filter(
            PatientAssessment.performed_by.ilike(
                f"%{filters['staff_name']}%"
            )
        )
    if filters["staff_role"] and filters["staff_role"] != "nurse":
        assessment_query = assessment_query.filter(False)
    for assessment in assessment_query.all():
        if assessment.visit_id and assessment.visit_id not in visit_ids:
            continue
        name = assessment.performed_by or "Unassigned"
        matching_keys = [key for key in staff if key[0] == name]
        key = matching_keys[0] if matching_keys else (name, "nurse")
        staff[key]["staff_name"], staff[key]["staff_role"] = key
        staff[key]["assessments_completed"] += 1

    rows = sorted(
        staff.values(),
        key=lambda row: (-row["total_visits"], row["staff_name"]),
    )
    data = {
        "summary": {
            "total_staff": len(rows),
            "total_visits": sum(row["total_visits"] for row in rows),
            "total_notes": sum(
                row["aide_notes_completed"] + row["nurse_notes_completed"]
                for row in rows
            ),
            "total_assessments": sum(
                row["assessments_completed"] for row in rows
            ),
        },
        "groups": {
            "activity_by_role": _group_counts(
                row["staff_role"]
                for row in rows
                for _ in range(row["total_visits"])
            ),
        },
        "recent": rows[:10],
        "rows": rows,
    }
    return _respond(
        "staff-activity",
        data,
        [
            "staff_name",
            "staff_role",
            "total_visits",
            "aide_notes_completed",
            "nurse_notes_completed",
            "assessments_completed",
        ],
    )


@reports_bp.get("/assessment-summary")
@swag_from(assessment_summary_report_spec)
@_report_errors
def assessment_summary_report():
    filters = _filters()
    query = PatientAssessment.query
    if filters["start_date"]:
        query = query.filter(
            PatientAssessment.assessment_date >= filters["start_date"]
        )
    if filters["end_date"]:
        query = query.filter(
            PatientAssessment.assessment_date <= filters["end_date"]
        )
    if filters["patient_id"]:
        query = query.filter(
            PatientAssessment.patient_id == filters["patient_id"]
        )
    if filters["status"]:
        query = query.filter(PatientAssessment.status == filters["status"])
    assessments = query.order_by(
        PatientAssessment.assessment_date.desc(),
        PatientAssessment.id.desc(),
    ).all()
    rows = [
        {
            "assessment_id": assessment.id,
            "patient_name": _patient_name(assessment.patient),
            "assessment_date": assessment.assessment_date.isoformat(),
            "assessment_type": assessment.assessment_type,
            "status": assessment.status,
            "performed_by": assessment.performed_by or "",
            "linked_visit": "Yes" if assessment.visit_id else "No",
        }
        for assessment in assessments
    ]
    data = {
        "summary": {
            "total_assessments": len(assessments),
            "completed_assessments": sum(
                a.status == "completed" for a in assessments
            ),
            "draft_assessments": sum(a.status == "draft" for a in assessments),
            "linked_to_visits": sum(bool(a.visit_id) for a in assessments),
        },
        "groups": {
            "assessments_by_type": _group_counts(
                a.assessment_type for a in assessments
            ),
            "assessments_by_status": _group_counts(a.status for a in assessments),
        },
        "recent": rows[:10],
        "rows": rows,
    }
    return _respond(
        "assessment-summary",
        data,
        [
            "assessment_id",
            "patient_name",
            "assessment_date",
            "assessment_type",
            "status",
            "performed_by",
            "linked_visit",
        ],
    )


@reports_bp.get("/medical-records-summary")
@swag_from(medical_records_summary_report_spec)
@_report_errors
def medical_records_summary_report():
    filters = _filters()
    query = MedicalRecord.query
    if filters["start_date"]:
        query = query.filter(
            MedicalRecord.uploaded_at
            >= _date_boundary(filters["start_date"], time.min)
        )
    if filters["end_date"]:
        query = query.filter(
            MedicalRecord.uploaded_at
            <= _date_boundary(filters["end_date"], time.max)
        )
    if filters["patient_id"]:
        query = query.filter(MedicalRecord.patient_id == filters["patient_id"])
    if filters["visit_type"]:
        query = query.filter(MedicalRecord.record_type == filters["visit_type"])
    records = query.order_by(
        MedicalRecord.uploaded_at.desc(),
        MedicalRecord.id.desc(),
    ).all()
    rows = [
        {
            "record_id": record.id,
            "patient_name": _patient_name(record.patient),
            "title": record.title,
            "record_type": record.record_type or "",
            "file_name": record.file_name,
            "uploaded_by": record.uploaded_by or "",
            "uploaded_at": record.uploaded_at.date().isoformat(),
        }
        for record in records
    ]
    data = {
        "summary": {
            "total_records": len(records),
            "patients_with_records": len({record.patient_id for record in records}),
            "record_types": len(
                {record.record_type for record in records if record.record_type}
            ),
            "recent_uploads": len(rows[:10]),
        },
        "groups": {
            "records_by_type": _group_counts(r.record_type for r in records),
            "records_over_time": _date_groups(
                r.uploaded_at.date().isoformat() for r in records
            ),
        },
        "recent": rows[:10],
        "rows": rows,
    }
    return _respond(
        "medical-records-summary",
        data,
        [
            "record_id",
            "patient_name",
            "title",
            "record_type",
            "file_name",
            "uploaded_by",
            "uploaded_at",
        ],
    )
