from uuid import uuid4
from zipfile import BadZipFile, ZipFile

from flasgger import swag_from
from flask import Blueprint, Response, current_app, jsonify, request, stream_with_context
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import MedicalRecord, Patient
from app.storage import MedicalRecordStorageError, get_medical_record_storage
from app.swagger import (
    medical_record_create_spec,
    medical_record_delete_spec,
    medical_record_download_spec,
    medical_record_get_spec,
    medical_record_list_spec,
    medical_record_update_spec,
    patient_medical_records_list_spec,
)


medical_records_bp = Blueprint("medical_records", __name__, url_prefix="/api")

ALLOWED_FILE_TYPES = {
    "application/pdf": {".pdf"},
    "image/jpeg": {".jpg", ".jpeg"},
    "image/png": {".png"},
    "application/msword": {".doc"},
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        ".docx"
    },
}
EDITABLE_FIELDS = {"title", "description", "record_type", "uploaded_by"}


def success_response(data, message, status_code=200):
    return jsonify({"data": data, "message": message}), status_code


def error_response(message, status_code=400, errors=None):
    payload = {"message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status_code


def normalized_text(value):
    return value.strip() if isinstance(value, str) and value.strip() else None


def parse_patient_id(value):
    try:
        patient_id = int(value)
    except (TypeError, ValueError):
        return None
    return patient_id if patient_id > 0 else None


def file_size(file_storage):
    stream = file_storage.stream
    current_position = stream.tell()
    stream.seek(0, 2)
    size = stream.tell()
    stream.seek(current_position)
    return size


def file_content_matches_type(file_storage):
    stream = file_storage.stream
    stream.seek(0)
    signature = stream.read(8)
    stream.seek(0)

    if file_storage.mimetype == "application/pdf":
        return signature.startswith(b"%PDF-")
    if file_storage.mimetype == "image/jpeg":
        return signature.startswith(b"\xff\xd8\xff")
    if file_storage.mimetype == "image/png":
        return signature == b"\x89PNG\r\n\x1a\n"
    if file_storage.mimetype == "application/msword":
        return signature == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
    if (
        file_storage.mimetype
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        try:
            with ZipFile(stream) as archive:
                names = set(archive.namelist())
                return "[Content_Types].xml" in names and any(
                    name.startswith("word/") for name in names
                )
        except BadZipFile:
            return False
        finally:
            stream.seek(0)
    return False


def validate_upload():
    errors = {}
    patient_id = parse_patient_id(request.form.get("patient_id"))
    title = normalized_text(request.form.get("title"))
    upload = request.files.get("file")
    patient = None

    if patient_id is None:
        errors["patient_id"] = "This field is required and must be a valid integer."
    else:
        patient = db.session.get(Patient, patient_id)
        if patient is None:
            errors["patient_id"] = "Patient not found."

    if title is None:
        errors["title"] = "This field is required."

    if upload is None or not upload.filename:
        errors["file"] = "This field is required."
        return None, errors

    safe_name = secure_filename(upload.filename)
    extension = f".{safe_name.rsplit('.', 1)[-1].lower()}" if "." in safe_name else ""
    allowed_extensions = ALLOWED_FILE_TYPES.get(upload.mimetype)
    if not safe_name or not allowed_extensions or extension not in allowed_extensions:
        errors["file"] = "Use a PDF, JPEG, PNG, DOC, or DOCX file."
    elif not file_content_matches_type(upload):
        errors["file"] = "File content does not match the selected document type."

    size = file_size(upload)
    if size <= 0:
        errors["file"] = "The uploaded file is empty."
    elif size > current_app.config["MEDICAL_RECORD_MAX_FILE_SIZE"]:
        max_mb = current_app.config["MEDICAL_RECORD_MAX_FILE_SIZE"] // (1024 * 1024)
        errors["file"] = f"File size must not exceed {max_mb} MB."

    if errors:
        return None, errors

    upload.stream.seek(0)
    return {
        "patient": patient,
        "patient_id": patient_id,
        "title": title,
        "description": normalized_text(request.form.get("description")),
        "record_type": normalized_text(request.form.get("record_type")),
        "uploaded_by": normalized_text(request.form.get("uploaded_by")),
        "upload": upload,
        "file_name": safe_name,
        "file_size": size,
    }, {}


def parse_metadata_payload(payload):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}

    data = {}
    errors = {}
    for field in EDITABLE_FIELDS:
        if field in payload:
            data[field] = normalized_text(payload[field])

    if "title" in data and data["title"] is None:
        errors["title"] = "This field is required."

    return data, errors


@medical_records_bp.get("/medical-records")
@swag_from(medical_record_list_spec)
def list_medical_records():
    records = MedicalRecord.query.order_by(MedicalRecord.uploaded_at.desc()).all()
    return success_response(
        [record.to_dict() for record in records],
        "Medical records retrieved successfully",
    )


@medical_records_bp.get("/medical-records/<int:medical_record_id>")
@swag_from(medical_record_get_spec)
def get_medical_record(medical_record_id):
    record = db.session.get(MedicalRecord, medical_record_id)
    if record is None:
        return error_response("Medical record not found", 404)
    return success_response(record.to_dict(), "Medical record retrieved successfully")


@medical_records_bp.post("/medical-records")
@swag_from(medical_record_create_spec)
def create_medical_record():
    data, errors = validate_upload()
    if errors:
        return error_response("Invalid medical record data", 400, errors)

    object_key = f"patients/{data['patient_id']}/{uuid4().hex}_{data['file_name']}"
    storage = get_medical_record_storage()

    try:
        storage.upload(
            object_key,
            data["upload"].stream,
            data["file_size"],
            data["upload"].mimetype,
        )
    except MedicalRecordStorageError as exc:
        return error_response(str(exc), 502)

    record = MedicalRecord(
        patient_id=data["patient_id"],
        title=data["title"],
        description=data["description"],
        record_type=data["record_type"],
        file_name=data["file_name"],
        file_mime_type=data["upload"].mimetype,
        file_size=data["file_size"],
        storage_bucket=storage.bucket,
        storage_object_key=object_key,
        uploaded_by=data["uploaded_by"],
    )

    try:
        db.session.add(record)
        db.session.commit()
    except Exception:
        db.session.rollback()
        storage.delete(object_key)
        raise

    return success_response(
        record.to_dict(),
        "Medical record uploaded successfully",
        201,
    )


@medical_records_bp.put("/medical-records/<int:medical_record_id>")
@swag_from(medical_record_update_spec)
def update_medical_record(medical_record_id):
    record = db.session.get(MedicalRecord, medical_record_id)
    if record is None:
        return error_response("Medical record not found", 404)

    data, errors = parse_metadata_payload(request.get_json(silent=True))
    if errors:
        return error_response("Invalid medical record data", 400, errors)

    for field, value in data.items():
        setattr(record, field, value)
    db.session.commit()

    return success_response(
        record.to_dict(),
        "Medical record updated successfully",
    )


@medical_records_bp.delete("/medical-records/<int:medical_record_id>")
@swag_from(medical_record_delete_spec)
def delete_medical_record(medical_record_id):
    record = db.session.get(MedicalRecord, medical_record_id)
    if record is None:
        return error_response("Medical record not found", 404)

    try:
        get_medical_record_storage().delete(record.storage_object_key)
    except MedicalRecordStorageError as exc:
        return error_response(str(exc), 502)

    db.session.delete(record)
    db.session.commit()
    return success_response(
        {"id": medical_record_id},
        "Medical record deleted successfully",
    )


@medical_records_bp.get("/patients/<int:patient_id>/medical-records")
@swag_from(patient_medical_records_list_spec)
def list_patient_medical_records(patient_id):
    patient = db.session.get(Patient, patient_id)
    if patient is None:
        return error_response("Patient not found", 404)

    records = (
        MedicalRecord.query.filter_by(patient_id=patient_id)
        .order_by(MedicalRecord.uploaded_at.desc())
        .all()
    )
    return success_response(
        [record.to_dict() for record in records],
        "Patient medical records retrieved successfully",
    )


@medical_records_bp.get("/medical-records/<int:medical_record_id>/download")
@swag_from(medical_record_download_spec)
def download_medical_record(medical_record_id):
    record = db.session.get(MedicalRecord, medical_record_id)
    if record is None:
        return error_response("Medical record not found", 404)

    try:
        source = get_medical_record_storage().open(record.storage_object_key)
    except FileNotFoundError:
        return error_response("Stored medical record file not found", 404)
    except MedicalRecordStorageError as exc:
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

    response = Response(generate(), mimetype=record.file_mime_type)
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{record.file_name}"'
    )
    response.headers["Content-Length"] = str(record.file_size)
    return response
