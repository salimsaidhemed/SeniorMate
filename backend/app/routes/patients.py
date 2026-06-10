from datetime import UTC, date, datetime
from uuid import uuid4

from flasgger import swag_from
from flask import Blueprint, Response, current_app, jsonify, request, stream_with_context
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Patient
from app.storage import PrivateObjectStorageError, get_patient_photo_storage
from app.swagger import (
    patient_create_spec,
    patient_delete_spec,
    patient_get_spec,
    patient_list_spec,
    patient_photo_delete_spec,
    patient_photo_get_spec,
    patient_photo_upload_spec,
    patient_photo_verify_spec,
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
ALLOWED_PHOTO_TYPES = {
    "image/jpeg": {".jpg", ".jpeg"},
    "image/png": {".png"},
}


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


def upload_size(upload):
    stream = upload.stream
    current_position = stream.tell()
    stream.seek(0, 2)
    size = stream.tell()
    stream.seek(current_position)
    return size


def photo_content_matches_type(upload):
    upload.stream.seek(0)
    signature = upload.stream.read(8)
    upload.stream.seek(0)

    if upload.mimetype == "image/jpeg":
        return signature.startswith(b"\xff\xd8\xff")
    if upload.mimetype == "image/png":
        return signature == b"\x89PNG\r\n\x1a\n"
    return False


def validate_photo_upload():
    upload = request.files.get("file")
    errors = {}

    if upload is None or not upload.filename:
        return None, {"file": "This field is required."}

    safe_name = secure_filename(upload.filename)
    extension = f".{safe_name.rsplit('.', 1)[-1].lower()}" if "." in safe_name else ""
    allowed_extensions = ALLOWED_PHOTO_TYPES.get(upload.mimetype)

    if not safe_name or not allowed_extensions or extension not in allowed_extensions:
        errors["file"] = "Use a JPEG or PNG image."
    elif not photo_content_matches_type(upload):
        errors["file"] = "File content does not match the selected image type."

    size = upload_size(upload)
    if size <= 0:
        errors["file"] = "The uploaded image is empty."
    elif size > current_app.config["PATIENT_PHOTO_MAX_FILE_SIZE"]:
        max_mb = current_app.config["PATIENT_PHOTO_MAX_FILE_SIZE"] / (1024 * 1024)
        errors["file"] = f"Image size must not exceed {max_mb:g} MB."

    if errors:
        return None, errors

    upload.stream.seek(0)
    return {
        "upload": upload,
        "file_name": safe_name,
        "file_size": size,
    }, {}


def clear_photo_metadata(patient):
    patient.photo_object_key = None
    patient.photo_file_name = None
    patient.photo_mime_type = None
    patient.photo_file_size = None
    patient.photo_uploaded_at = None
    patient.photo_verified = False


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

    if patient.photo_object_key:
        try:
            get_patient_photo_storage().delete(patient.photo_object_key)
        except PrivateObjectStorageError as exc:
            return error_response(str(exc), 502)

    db.session.delete(patient)
    db.session.commit()

    return success_response({"id": patient_id}, "Patient deleted successfully")


@patients_bp.post("/<int:patient_id>/photo")
@swag_from(patient_photo_upload_spec)
def upload_patient_photo(patient_id):
    patient = db.session.get(Patient, patient_id)
    if patient is None:
        return error_response("Patient not found", 404)

    data, errors = validate_photo_upload()
    if errors:
        return error_response("Invalid patient photo", 400, errors)

    extension = f".{data['file_name'].rsplit('.', 1)[-1].lower()}"
    object_key = f"patients/{patient.id}/profile/{uuid4().hex}{extension}"
    previous_object_key = patient.photo_object_key
    storage = get_patient_photo_storage()

    try:
        storage.upload(
            object_key,
            data["upload"].stream,
            data["file_size"],
            data["upload"].mimetype,
        )
    except PrivateObjectStorageError as exc:
        return error_response(str(exc), 502)

    patient.photo_object_key = object_key
    patient.photo_file_name = data["file_name"]
    patient.photo_mime_type = data["upload"].mimetype
    patient.photo_file_size = data["file_size"]
    patient.photo_uploaded_at = datetime.now(UTC)
    patient.photo_verified = False

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        storage.delete(object_key)
        raise

    if previous_object_key and previous_object_key != object_key:
        try:
            storage.delete(previous_object_key)
        except PrivateObjectStorageError:
            current_app.logger.warning(
                "Patient photo replacement left stale object %s",
                previous_object_key,
            )

    return success_response(
        patient.to_dict(),
        "Patient photo uploaded successfully",
        201,
    )


@patients_bp.get("/<int:patient_id>/photo")
@swag_from(patient_photo_get_spec)
def get_patient_photo(patient_id):
    patient = db.session.get(Patient, patient_id)
    if patient is None:
        return error_response("Patient not found", 404)
    if not patient.photo_object_key:
        return error_response("Patient photo not found", 404)

    try:
        source = get_patient_photo_storage().open(patient.photo_object_key)
    except FileNotFoundError:
        return error_response("Stored patient photo not found", 404)
    except PrivateObjectStorageError as exc:
        return error_response(str(exc), 502)

    @stream_with_context
    def generate():
        try:
            while chunk := source.read(64 * 1024):
                yield chunk
        finally:
            source.close()
            if hasattr(source, "release_conn"):
                source.release_conn()

    response = Response(generate(), mimetype=patient.photo_mime_type)
    response.headers["Content-Disposition"] = (
        f'inline; filename="{patient.photo_file_name}"'
    )
    response.headers["Content-Length"] = str(patient.photo_file_size)
    response.headers["Cache-Control"] = "private, max-age=300"
    return response


@patients_bp.patch("/<int:patient_id>/photo/verify")
@swag_from(patient_photo_verify_spec)
def verify_patient_photo(patient_id):
    patient = db.session.get(Patient, patient_id)
    if patient is None:
        return error_response("Patient not found", 404)
    if not patient.photo_object_key:
        return error_response("Patient photo not found", 404)

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("verified"), bool):
        return error_response(
            "Invalid patient photo verification",
            400,
            {"verified": "A boolean value is required."},
        )

    patient.photo_verified = payload["verified"]
    db.session.commit()
    return success_response(
        patient.to_dict(),
        "Patient photo verification updated successfully",
    )


@patients_bp.delete("/<int:patient_id>/photo")
@swag_from(patient_photo_delete_spec)
def delete_patient_photo(patient_id):
    patient = db.session.get(Patient, patient_id)
    if patient is None:
        return error_response("Patient not found", 404)
    if not patient.photo_object_key:
        return error_response("Patient photo not found", 404)

    try:
        get_patient_photo_storage().delete(patient.photo_object_key)
    except PrivateObjectStorageError as exc:
        return error_response(str(exc), 502)

    clear_photo_metadata(patient)
    db.session.commit()
    return success_response(
        patient.to_dict(),
        "Patient photo deleted successfully",
    )
