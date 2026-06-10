from datetime import date, time

from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import AideNote, Patient, Visit
from app.routes.query_utils import (
    end_of_day,
    paginated_response,
    parse_iso_date,
    start_of_day,
)
from app.swagger import (
    aide_note_create_spec,
    aide_note_delete_spec,
    aide_note_get_spec,
    aide_note_list_spec,
    aide_note_update_spec,
    patient_aide_notes_list_spec,
    visit_aide_note_get_spec,
)


aide_notes_bp = Blueprint("aide_notes", __name__, url_prefix="/api")

JSON_FIELDS = {
    "personal_care",
    "nutrition",
    "mental_status",
    "elimination",
    "activity",
    "assistive_devices",
    "housekeeping",
}
AIDE_NOTE_FIELDS = {
    "patient_id",
    "visit_id",
    "additional_notes",
    "aide_name",
    "signature_data",
    "signature_date",
    "time_in",
    "time_out",
    *JSON_FIELDS,
}


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


def parse_aide_note_payload(payload, partial=False, current_note=None):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}

    data = {}
    errors = {}
    patient = None
    visit = None

    for field in AIDE_NOTE_FIELDS:
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
        existing_note = AideNote.query.filter_by(visit_id=visit.id).first()
        if existing_note is not None and (
            current_note is None or existing_note.id != current_note.id
        ):
            errors["visit_id"] = "An aide note already exists for this visit."

    if not partial or "aide_name" in data:
        aide_name = data.get("aide_name")
        if not isinstance(aide_name, str) or not aide_name.strip():
            errors["aide_name"] = "This field is required."
        else:
            data["aide_name"] = aide_name.strip()

    for field in JSON_FIELDS:
        if field in data and data[field] is not None and not isinstance(
            data[field],
            (dict, list),
        ):
            errors[field] = "Checklist data must be a JSON object or array."

    for field in ("additional_notes", "signature_data"):
        if field in data and isinstance(data[field], str):
            data[field] = data[field].strip() or None

    if "signature_date" in data and data["signature_date"]:
        try:
            data["signature_date"] = date.fromisoformat(data["signature_date"])
        except (TypeError, ValueError):
            errors["signature_date"] = "Use ISO date format YYYY-MM-DD."
    elif "signature_date" in data:
        data["signature_date"] = None

    for field in ("time_in", "time_out"):
        if field in data:
            try:
                data[field] = parse_time(data[field])
            except ValueError:
                errors[field] = "Use 24-hour time format HH:MM."

    return data, errors


@aide_notes_bp.get("/aide-notes")
@swag_from(aide_note_list_spec)
def list_aide_notes():
    query = AideNote.query
    patient_id = request.args.get("patient_id", "").strip()
    visit_id = request.args.get("visit_id", "").strip()
    aide_name = request.args.get("aide_name", "").strip()
    start_date = parse_iso_date(request.args.get("start_date"))
    end_date = parse_iso_date(request.args.get("end_date"))

    if patient_id:
        query = query.filter(AideNote.patient_id == int(patient_id))

    if visit_id:
        query = query.filter(AideNote.visit_id == int(visit_id))

    if aide_name:
        query = query.filter(AideNote.aide_name.ilike(f"%{aide_name}%"))

    if start_date:
        query = query.filter(AideNote.created_at >= start_of_day(start_date))

    if end_date:
        query = query.filter(AideNote.created_at <= end_of_day(end_date))

    return paginated_response(
        query.order_by(AideNote.id.desc()),
        lambda aide_note: aide_note.to_dict(),
        "Aide notes retrieved successfully",
    )


@aide_notes_bp.get("/aide-notes/<int:aide_note_id>")
@swag_from(aide_note_get_spec)
def get_aide_note(aide_note_id):
    aide_note = db.session.get(AideNote, aide_note_id)

    if aide_note is None:
        return error_response("Aide note not found", 404)

    return success_response(aide_note.to_dict(), "Aide note retrieved successfully")


@aide_notes_bp.post("/aide-notes")
@swag_from(aide_note_create_spec)
def create_aide_note():
    data, errors = parse_aide_note_payload(request.get_json(silent=True))

    if errors:
        return error_response("Invalid aide note data", 400, errors)

    aide_note = AideNote(**data)
    db.session.add(aide_note)
    db.session.commit()

    return success_response(aide_note.to_dict(), "Aide note created successfully", 201)


@aide_notes_bp.put("/aide-notes/<int:aide_note_id>")
@swag_from(aide_note_update_spec)
def update_aide_note(aide_note_id):
    aide_note = db.session.get(AideNote, aide_note_id)

    if aide_note is None:
        return error_response("Aide note not found", 404)

    data, errors = parse_aide_note_payload(
        request.get_json(silent=True),
        partial=True,
        current_note=aide_note,
    )

    if errors:
        return error_response("Invalid aide note data", 400, errors)

    for field, value in data.items():
        setattr(aide_note, field, value)

    db.session.commit()

    return success_response(aide_note.to_dict(), "Aide note updated successfully")


@aide_notes_bp.delete("/aide-notes/<int:aide_note_id>")
@swag_from(aide_note_delete_spec)
def delete_aide_note(aide_note_id):
    aide_note = db.session.get(AideNote, aide_note_id)

    if aide_note is None:
        return error_response("Aide note not found", 404)

    db.session.delete(aide_note)
    db.session.commit()

    return success_response({"id": aide_note_id}, "Aide note deleted successfully")


@aide_notes_bp.get("/patients/<int:patient_id>/aide-notes")
@swag_from(patient_aide_notes_list_spec)
def list_patient_aide_notes(patient_id):
    patient = db.session.get(Patient, patient_id)

    if patient is None:
        return error_response("Patient not found", 404)

    aide_notes = (
        AideNote.query.filter_by(patient_id=patient_id).order_by(AideNote.id.desc()).all()
    )

    return success_response(
        [aide_note.to_dict() for aide_note in aide_notes],
        "Patient aide notes retrieved successfully",
    )


@aide_notes_bp.get("/visits/<int:visit_id>/aide-note")
@swag_from(visit_aide_note_get_spec)
def get_visit_aide_note(visit_id):
    visit = db.session.get(Visit, visit_id)

    if visit is None:
        return error_response("Visit not found", 404)

    aide_note = AideNote.query.filter_by(visit_id=visit_id).first()

    if aide_note is None:
        return error_response("Aide note not found", 404)

    return success_response(aide_note.to_dict(), "Visit aide note retrieved successfully")
