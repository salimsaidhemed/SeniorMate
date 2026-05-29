from datetime import date

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Patient
from app.swagger import (
    patient_create_spec,
    patient_delete_spec,
    patient_get_spec,
    patient_list_spec,
    patient_update_spec,
)


patients_bp = Blueprint("patients", __name__, url_prefix="/api/patients")

PATIENT_FIELDS = {
    "first_name",
    "last_name",
    "date_of_birth",
    "gender",
    "phone",
    "email",
    "address",
    "emergency_contact_name",
    "emergency_contact_phone",
    "diagnosis_summary",
    "status",
}
VALID_STATUSES = {"active", "inactive"}


def success_response(data, message, status_code=200):
    return jsonify({"data": data, "message": message}), status_code


def error_response(message, status_code=400, errors=None):
    payload = {"message": message}

    if errors:
        payload["errors"] = errors

    return jsonify(payload), status_code


def parse_patient_payload(payload, partial=False):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}

    data = {}
    errors = {}

    for field in PATIENT_FIELDS:
        if field in payload:
            data[field] = payload[field]

    for field in ("first_name", "last_name"):
        value = data.get(field)
        if not partial or field in data:
            if not isinstance(value, str) or not value.strip():
                errors[field] = "This field is required."
            elif field in data:
                data[field] = value.strip()

    if "status" not in data and not partial:
        data["status"] = "active"

    if "status" in data and data["status"] not in VALID_STATUSES:
        errors["status"] = "Status must be active or inactive."

    if "date_of_birth" in data and data["date_of_birth"]:
        try:
            data["date_of_birth"] = date.fromisoformat(data["date_of_birth"])
        except (TypeError, ValueError):
            errors["date_of_birth"] = "Use ISO date format YYYY-MM-DD."
    elif "date_of_birth" in data:
        data["date_of_birth"] = None

    return data, errors


@patients_bp.get("")
@swag_from(patient_list_spec)
def list_patients():
    patients = Patient.query.order_by(Patient.id.asc()).all()

    return success_response(
        [patient.to_dict() for patient in patients],
        "Patients retrieved successfully",
    )


@patients_bp.get("/<int:patient_id>")
@swag_from(patient_get_spec)
def get_patient(patient_id):
    patient = db.session.get(Patient, patient_id)

    if patient is None:
        return error_response("Patient not found", 404)

    return success_response(patient.to_dict(), "Patient retrieved successfully")


@patients_bp.post("")
@swag_from(patient_create_spec)
def create_patient():
    data, errors = parse_patient_payload(request.get_json(silent=True))

    if errors:
        return error_response("Invalid patient data", 400, errors)

    patient = Patient(**data)
    db.session.add(patient)
    db.session.commit()

    return success_response(patient.to_dict(), "Patient created successfully", 201)


@patients_bp.put("/<int:patient_id>")
@swag_from(patient_update_spec)
def update_patient(patient_id):
    patient = db.session.get(Patient, patient_id)

    if patient is None:
        return error_response("Patient not found", 404)

    data, errors = parse_patient_payload(request.get_json(silent=True), partial=True)

    if errors:
        return error_response("Invalid patient data", 400, errors)

    for field, value in data.items():
        setattr(patient, field, value)

    db.session.commit()

    return success_response(patient.to_dict(), "Patient updated successfully")


@patients_bp.delete("/<int:patient_id>")
@swag_from(patient_delete_spec)
def delete_patient(patient_id):
    patient = db.session.get(Patient, patient_id)

    if patient is None:
        return error_response("Patient not found", 404)

    db.session.delete(patient)
    db.session.commit()

    return success_response({"id": patient_id}, "Patient deleted successfully")
