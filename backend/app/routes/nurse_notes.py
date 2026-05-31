from datetime import date

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import NurseNote, Patient, Visit
from app.swagger import (
    nurse_note_create_spec,
    nurse_note_delete_spec,
    nurse_note_get_spec,
    nurse_note_list_spec,
    nurse_note_update_spec,
    patient_nurse_notes_list_spec,
    visit_nurse_note_get_spec,
)


nurse_notes_bp = Blueprint("nurse_notes", __name__, url_prefix="/api")

JSON_FIELDS = {
    "living_arrangements",
    "visit_type",
    "vital_signs",
    "diet",
    "pain_assessment",
    "sensory",
    "neuro",
    "respiratory",
    "cardiac",
    "peripheral_circulation",
    "genitourinary",
    "gastrointestinal",
    "endocrine",
    "skin_integrity",
    "wound_evaluation",
    "mental_status",
    "functional_status",
    "homebound_status",
    "patient_caregiver_understanding",
    "md_contact",
}
TEXT_FIELDS = {
    "diagnosis",
    "skilled_nursing",
    "response_to_intervention",
    "discharge_planning",
    "patient_feedback",
    "narrative",
    "signature_data",
}
NURSE_NOTE_FIELDS = {
    "patient_id",
    "visit_id",
    "signature_date",
    *JSON_FIELDS,
    *TEXT_FIELDS,
}


def success_response(data, message, status_code=200):
    return jsonify({"data": data, "message": message}), status_code


def error_response(message, status_code=400, errors=None):
    payload = {"message": message}

    if errors:
        payload["errors"] = errors

    return jsonify(payload), status_code


def parse_nurse_note_payload(payload, partial=False, current_note=None):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}

    data = {}
    errors = {}
    patient = None
    visit = None

    for field in NURSE_NOTE_FIELDS:
        if field in payload:
            data[field] = payload[field]

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

    if partial and "patient_id" not in data and current_note is not None:
        patient = db.session.get(Patient, current_note.patient_id)

    if not partial or "visit_id" in data:
        visit_id = data.get("visit_id")
        if visit_id in (None, ""):
            errors["visit_id"] = "This field is required."
        elif not isinstance(visit_id, int):
            errors["visit_id"] = "Visit ID must be an integer."
        else:
            visit = db.session.get(Visit, visit_id)
            if visit is None:
                errors["visit_id"] = "Visit not found."

    if partial and "visit_id" not in data and current_note is not None:
        visit = db.session.get(Visit, current_note.visit_id)

    if patient is not None and visit is not None and visit.patient_id != patient.id:
        errors["visit_id"] = "Visit does not belong to the selected patient."

    if visit is not None:
        existing_note = NurseNote.query.filter_by(visit_id=visit.id).first()
        if existing_note is not None and (
            current_note is None or existing_note.id != current_note.id
        ):
            errors["visit_id"] = "A nurse note already exists for this visit."

    for field in JSON_FIELDS:
        if field in data and data[field] is not None and not isinstance(
            data[field],
            (dict, list),
        ):
            errors[field] = "Clinical section data must be a JSON object or array."

    for field in TEXT_FIELDS:
        if field in data and isinstance(data[field], str):
            data[field] = data[field].strip() or None

    if "signature_date" in data and data["signature_date"]:
        try:
            data["signature_date"] = date.fromisoformat(data["signature_date"])
        except (TypeError, ValueError):
            errors["signature_date"] = "Use ISO date format YYYY-MM-DD."
    elif "signature_date" in data:
        data["signature_date"] = None

    return data, errors


@nurse_notes_bp.get("/nurse-notes")
@swag_from(nurse_note_list_spec)
def list_nurse_notes():
    nurse_notes = NurseNote.query.order_by(NurseNote.id.desc()).all()

    return success_response(
        [nurse_note.to_dict() for nurse_note in nurse_notes],
        "Nurse notes retrieved successfully",
    )


@nurse_notes_bp.get("/nurse-notes/<int:nurse_note_id>")
@swag_from(nurse_note_get_spec)
def get_nurse_note(nurse_note_id):
    nurse_note = db.session.get(NurseNote, nurse_note_id)

    if nurse_note is None:
        return error_response("Nurse note not found", 404)

    return success_response(nurse_note.to_dict(), "Nurse note retrieved successfully")


@nurse_notes_bp.post("/nurse-notes")
@swag_from(nurse_note_create_spec)
def create_nurse_note():
    data, errors = parse_nurse_note_payload(request.get_json(silent=True))

    if errors:
        return error_response("Invalid nurse note data", 400, errors)

    nurse_note = NurseNote(**data)
    db.session.add(nurse_note)
    db.session.commit()

    return success_response(nurse_note.to_dict(), "Nurse note created successfully", 201)


@nurse_notes_bp.put("/nurse-notes/<int:nurse_note_id>")
@swag_from(nurse_note_update_spec)
def update_nurse_note(nurse_note_id):
    nurse_note = db.session.get(NurseNote, nurse_note_id)

    if nurse_note is None:
        return error_response("Nurse note not found", 404)

    data, errors = parse_nurse_note_payload(
        request.get_json(silent=True),
        partial=True,
        current_note=nurse_note,
    )

    if errors:
        return error_response("Invalid nurse note data", 400, errors)

    for field, value in data.items():
        setattr(nurse_note, field, value)

    db.session.commit()

    return success_response(nurse_note.to_dict(), "Nurse note updated successfully")


@nurse_notes_bp.delete("/nurse-notes/<int:nurse_note_id>")
@swag_from(nurse_note_delete_spec)
def delete_nurse_note(nurse_note_id):
    nurse_note = db.session.get(NurseNote, nurse_note_id)

    if nurse_note is None:
        return error_response("Nurse note not found", 404)

    db.session.delete(nurse_note)
    db.session.commit()

    return success_response({"id": nurse_note_id}, "Nurse note deleted successfully")


@nurse_notes_bp.get("/patients/<int:patient_id>/nurse-notes")
@swag_from(patient_nurse_notes_list_spec)
def list_patient_nurse_notes(patient_id):
    patient = db.session.get(Patient, patient_id)

    if patient is None:
        return error_response("Patient not found", 404)

    nurse_notes = (
        NurseNote.query.filter_by(patient_id=patient_id)
        .order_by(NurseNote.id.desc())
        .all()
    )

    return success_response(
        [nurse_note.to_dict() for nurse_note in nurse_notes],
        "Patient nurse notes retrieved successfully",
    )


@nurse_notes_bp.get("/visits/<int:visit_id>/nurse-note")
@swag_from(visit_nurse_note_get_spec)
def get_visit_nurse_note(visit_id):
    visit = db.session.get(Visit, visit_id)

    if visit is None:
        return error_response("Visit not found", 404)

    nurse_note = NurseNote.query.filter_by(visit_id=visit_id).first()

    if nurse_note is None:
        return error_response("Nurse note not found", 404)

    return success_response(nurse_note.to_dict(), "Visit nurse note retrieved successfully")
