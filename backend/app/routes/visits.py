from datetime import date, time

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Patient, Visit
from app.swagger import (
    patient_visits_list_spec,
    visit_create_spec,
    visit_delete_spec,
    visit_get_spec,
    visit_list_spec,
    visit_update_spec,
)


visits_bp = Blueprint("visits", __name__, url_prefix="/api")

VISIT_FIELDS = {
    "patient_id",
    "visit_date",
    "visit_type",
    "staff_name",
    "staff_role",
    "time_in",
    "time_out",
    "notes",
    "status",
}
VALID_STAFF_ROLES = {"aide", "nurse"}
VALID_STATUSES = {"scheduled", "completed", "cancelled"}


def success_response(data, message, status_code=200):
    return jsonify({"data": data, "message": message}), status_code


def error_response(message, status_code=400, errors=None):
    payload = {"message": message}

    if errors:
        payload["errors"] = errors

    return jsonify(payload), status_code


def parse_time(value):
    if value is None or value == "":
        return None

    if not isinstance(value, str):
        raise ValueError

    return time.fromisoformat(value)


def parse_visit_payload(payload, partial=False):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}

    data = {}
    errors = {}

    for field in VISIT_FIELDS:
        if field in payload:
            data[field] = payload[field]

    if not partial or "patient_id" in data:
        patient_id = data.get("patient_id")
        if patient_id in (None, ""):
            errors["patient_id"] = "This field is required."
        elif not isinstance(patient_id, int):
            errors["patient_id"] = "Patient ID must be an integer."
        elif db.session.get(Patient, patient_id) is None:
            errors["patient_id"] = "Patient not found."

    if not partial or "visit_date" in data:
        visit_date = data.get("visit_date")
        if not visit_date:
            errors["visit_date"] = "This field is required."
        else:
            try:
                data["visit_date"] = date.fromisoformat(visit_date)
            except (TypeError, ValueError):
                errors["visit_date"] = "Use ISO date format YYYY-MM-DD."

    if not partial or "visit_type" in data:
        visit_type = data.get("visit_type")
        if not isinstance(visit_type, str) or not visit_type.strip():
            errors["visit_type"] = "This field is required."
        else:
            data["visit_type"] = visit_type.strip()

    for field in ("staff_name", "notes"):
        if field in data and isinstance(data[field], str):
            data[field] = data[field].strip() or None

    if "staff_role" in data and data["staff_role"]:
        if not isinstance(data["staff_role"], str):
            errors["staff_role"] = "Staff role must be aide or nurse."
        else:
            data["staff_role"] = data["staff_role"].strip().lower()
            if data["staff_role"] not in VALID_STAFF_ROLES:
                errors["staff_role"] = "Staff role must be aide or nurse."
    elif "staff_role" in data:
        data["staff_role"] = None

    for field in ("time_in", "time_out"):
        if field in data:
            try:
                data[field] = parse_time(data[field])
            except ValueError:
                errors[field] = "Use 24-hour time format HH:MM."

    if "status" not in data and not partial:
        data["status"] = "scheduled"

    if "status" in data and data["status"] not in VALID_STATUSES:
        errors["status"] = "Status must be scheduled, completed, or cancelled."

    return data, errors


@visits_bp.get("/visits")
@swag_from(visit_list_spec)
def list_visits():
    visits = Visit.query.order_by(Visit.visit_date.desc(), Visit.id.desc()).all()

    return success_response(
        [visit.to_dict() for visit in visits],
        "Visits retrieved successfully",
    )


@visits_bp.get("/visits/<int:visit_id>")
@swag_from(visit_get_spec)
def get_visit(visit_id):
    visit = db.session.get(Visit, visit_id)

    if visit is None:
        return error_response("Visit not found", 404)

    return success_response(visit.to_dict(), "Visit retrieved successfully")


@visits_bp.post("/visits")
@swag_from(visit_create_spec)
def create_visit():
    data, errors = parse_visit_payload(request.get_json(silent=True))

    if errors:
        return error_response("Invalid visit data", 400, errors)

    visit = Visit(**data)
    db.session.add(visit)
    db.session.commit()

    return success_response(visit.to_dict(), "Visit created successfully", 201)


@visits_bp.put("/visits/<int:visit_id>")
@swag_from(visit_update_spec)
def update_visit(visit_id):
    visit = db.session.get(Visit, visit_id)

    if visit is None:
        return error_response("Visit not found", 404)

    data, errors = parse_visit_payload(request.get_json(silent=True), partial=True)

    if errors:
        return error_response("Invalid visit data", 400, errors)

    for field, value in data.items():
        setattr(visit, field, value)

    db.session.commit()

    return success_response(visit.to_dict(), "Visit updated successfully")


@visits_bp.delete("/visits/<int:visit_id>")
@swag_from(visit_delete_spec)
def delete_visit(visit_id):
    visit = db.session.get(Visit, visit_id)

    if visit is None:
        return error_response("Visit not found", 404)

    db.session.delete(visit)
    db.session.commit()

    return success_response({"id": visit_id}, "Visit deleted successfully")


@visits_bp.get("/patients/<int:patient_id>/visits")
@swag_from(patient_visits_list_spec)
def list_patient_visits(patient_id):
    patient = db.session.get(Patient, patient_id)

    if patient is None:
        return error_response("Patient not found", 404)

    visits = (
        Visit.query.filter_by(patient_id=patient_id)
        .order_by(Visit.visit_date.desc(), Visit.id.desc())
        .all()
    )

    return success_response(
        [visit.to_dict() for visit in visits],
        "Patient visits retrieved successfully",
    )
