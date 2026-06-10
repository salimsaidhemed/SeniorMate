from datetime import date

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Patient, PatientAssessment, Visit
from app.swagger import (
    assessment_create_spec,
    assessment_delete_spec,
    assessment_get_spec,
    assessment_list_spec,
    assessment_update_spec,
    patient_assessments_list_spec,
    visit_assessments_list_spec,
)


assessments_bp = Blueprint("assessments", __name__, url_prefix="/api")

ASSESSMENT_TYPES = {
    "fall_risk",
    "nutrition",
    "mobility",
    "cognitive",
    "general",
}
ASSESSMENT_STATUSES = {"draft", "completed"}
ASSESSMENT_FIELDS = {
    "patient_id",
    "visit_id",
    "assessment_type",
    "assessment_date",
    "performed_by",
    "summary",
    "findings",
    "recommendations",
    "status",
}


def success_response(data, message, status_code=200):
    return jsonify({"data": data, "message": message}), status_code


def error_response(message, status_code=400, errors=None):
    payload = {"message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status_code


def parse_assessment_payload(payload, partial=False, current_assessment=None):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}

    data = {field: payload[field] for field in ASSESSMENT_FIELDS if field in payload}
    errors = {}
    patient = None
    visit = None

    if not partial or "patient_id" in data:
        patient_id = data.get("patient_id")
        if patient_id in (None, ""):
            errors["patient_id"] = "This field is required."
        elif not isinstance(patient_id, int):
            errors["patient_id"] = "Patient ID must be an integer."
        else:
            patient = db.session.get(Patient, patient_id)
            if patient is None:
                errors["patient_id"] = "Patient not found."
    elif current_assessment is not None:
        patient = db.session.get(Patient, current_assessment.patient_id)

    if "visit_id" in data and data["visit_id"] not in (None, ""):
        if not isinstance(data["visit_id"], int):
            errors["visit_id"] = "Visit ID must be an integer."
        else:
            visit = db.session.get(Visit, data["visit_id"])
            if visit is None:
                errors["visit_id"] = "Visit not found."
    elif "visit_id" in data:
        data["visit_id"] = None
    elif current_assessment is not None and current_assessment.visit_id is not None:
        visit = db.session.get(Visit, current_assessment.visit_id)

    if patient is not None and visit is not None and visit.patient_id != patient.id:
        errors["visit_id"] = "Visit does not belong to the selected patient."

    if not partial or "assessment_type" in data:
        assessment_type = data.get("assessment_type")
        if not isinstance(assessment_type, str) or not assessment_type.strip():
            errors["assessment_type"] = "This field is required."
        elif assessment_type not in ASSESSMENT_TYPES:
            errors["assessment_type"] = "Select a supported assessment type."

    if not partial or "assessment_date" in data:
        assessment_date = data.get("assessment_date")
        if assessment_date in (None, ""):
            errors["assessment_date"] = "This field is required."
        else:
            try:
                data["assessment_date"] = date.fromisoformat(assessment_date)
            except (TypeError, ValueError):
                errors["assessment_date"] = "Use ISO date format YYYY-MM-DD."

    if "status" in data:
        if data["status"] not in ASSESSMENT_STATUSES:
            errors["status"] = "Status must be draft or completed."
    elif not partial:
        data["status"] = "draft"

    if (
        "findings" in data
        and data["findings"] is not None
        and not isinstance(data["findings"], (dict, list))
    ):
        errors["findings"] = "Findings must be a JSON object or array."

    for field in ("performed_by", "summary", "recommendations"):
        if field in data and isinstance(data[field], str):
            data[field] = data[field].strip() or None

    return data, errors


@assessments_bp.get("/assessments")
@swag_from(assessment_list_spec)
def list_assessments():
    assessments = PatientAssessment.query.order_by(
        PatientAssessment.assessment_date.desc(),
        PatientAssessment.id.desc(),
    ).all()
    return success_response(
        [assessment.to_dict() for assessment in assessments],
        "Assessments retrieved successfully",
    )


@assessments_bp.get("/assessments/<int:assessment_id>")
@swag_from(assessment_get_spec)
def get_assessment(assessment_id):
    assessment = db.session.get(PatientAssessment, assessment_id)
    if assessment is None:
        return error_response("Assessment not found", 404)
    return success_response(
        assessment.to_dict(),
        "Assessment retrieved successfully",
    )


@assessments_bp.post("/assessments")
@swag_from(assessment_create_spec)
def create_assessment():
    data, errors = parse_assessment_payload(request.get_json(silent=True))
    if errors:
        return error_response("Invalid assessment data", 400, errors)

    assessment = PatientAssessment(**data)
    db.session.add(assessment)
    db.session.commit()
    return success_response(
        assessment.to_dict(),
        "Assessment created successfully",
        201,
    )


@assessments_bp.put("/assessments/<int:assessment_id>")
@swag_from(assessment_update_spec)
def update_assessment(assessment_id):
    assessment = db.session.get(PatientAssessment, assessment_id)
    if assessment is None:
        return error_response("Assessment not found", 404)

    data, errors = parse_assessment_payload(
        request.get_json(silent=True),
        partial=True,
        current_assessment=assessment,
    )
    if errors:
        return error_response("Invalid assessment data", 400, errors)

    for field, value in data.items():
        setattr(assessment, field, value)
    db.session.commit()
    return success_response(
        assessment.to_dict(),
        "Assessment updated successfully",
    )


@assessments_bp.delete("/assessments/<int:assessment_id>")
@swag_from(assessment_delete_spec)
def delete_assessment(assessment_id):
    assessment = db.session.get(PatientAssessment, assessment_id)
    if assessment is None:
        return error_response("Assessment not found", 404)

    db.session.delete(assessment)
    db.session.commit()
    return success_response(
        {"id": assessment_id},
        "Assessment deleted successfully",
    )


@assessments_bp.get("/patients/<int:patient_id>/assessments")
@swag_from(patient_assessments_list_spec)
def list_patient_assessments(patient_id):
    patient = db.session.get(Patient, patient_id)
    if patient is None:
        return error_response("Patient not found", 404)

    assessments = (
        PatientAssessment.query.filter_by(patient_id=patient_id)
        .order_by(
            PatientAssessment.assessment_date.desc(),
            PatientAssessment.id.desc(),
        )
        .all()
    )
    return success_response(
        [assessment.to_dict() for assessment in assessments],
        "Patient assessments retrieved successfully",
    )


@assessments_bp.get("/visits/<int:visit_id>/assessments")
@swag_from(visit_assessments_list_spec)
def list_visit_assessments(visit_id):
    visit = db.session.get(Visit, visit_id)
    if visit is None:
        return error_response("Visit not found", 404)

    assessments = (
        PatientAssessment.query.filter_by(visit_id=visit_id)
        .order_by(
            PatientAssessment.assessment_date.desc(),
            PatientAssessment.id.desc(),
        )
        .all()
    )
    return success_response(
        [assessment.to_dict() for assessment in assessments],
        "Visit assessments retrieved successfully",
    )
