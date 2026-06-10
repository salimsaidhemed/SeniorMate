import re
from uuid import uuid4
from xml.etree import ElementTree

from flasgger import swag_from
from flask import Blueprint, Response, current_app, jsonify, request, stream_with_context
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import OrganizationSettings
from app.storage import PrivateObjectStorageError, get_branding_logo_storage
from app.swagger import (
    branding_delete_logo_spec,
    branding_get_spec,
    branding_public_get_spec,
    branding_public_logo_spec,
    branding_update_spec,
    branding_upload_logo_spec,
)


branding_bp = Blueprint("branding", __name__, url_prefix="/api")

DEFAULT_BRANDING = {
    "organization_name": "",
    "app_display_name": "SeniorMate",
    "primary_color": "#1F6F68",
    "secondary_color": "#4D6D78",
    "accent_color": "#32817A",
    "sidebar_color": "#FFFFFF",
    "login_banner_text": "",
    "footer_text": "",
}
TEXT_FIELDS = {
    "organization_name",
    "app_display_name",
    "login_banner_text",
    "footer_text",
}
COLOR_FIELDS = {
    "primary_color",
    "secondary_color",
    "accent_color",
    "sidebar_color",
}
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
ALLOWED_LOGO_TYPES = {
    "image/svg+xml": {".svg"},
    "image/png": {".png"},
    "image/jpeg": {".jpg", ".jpeg"},
}


def success_response(data, message, status_code=200):
    return jsonify({"data": data, "message": message}), status_code


def error_response(message, status_code=400, errors=None):
    payload = {"message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status_code


def get_settings(create=False):
    settings = db.session.get(OrganizationSettings, 1)
    if settings is None and create:
        settings = OrganizationSettings(id=1)
        db.session.add(settings)
    return settings


def resolved_branding(settings=None):
    resolved = dict(DEFAULT_BRANDING)
    if settings is not None:
        for field in DEFAULT_BRANDING:
            value = getattr(settings, field)
            if value:
                resolved[field] = value
    resolved.update(
        {
            "has_custom_logo": bool(settings and settings.logo_object_key),
            "logo_file_name": settings.logo_file_name if settings else None,
            "logo_url": (
                "/api/public/branding/logo"
                if settings and settings.logo_object_key
                else None
            ),
            "updated_at": (
                settings.updated_at.isoformat()
                if settings and settings.updated_at
                else None
            ),
        }
    )
    return resolved


def settings_response(settings):
    payload = resolved_branding(settings)
    if settings is not None:
        payload.update(settings.to_dict())
        for field, default in DEFAULT_BRANDING.items():
            payload[field] = getattr(settings, field) or default
        payload["logo_url"] = (
            "/api/public/branding/logo" if settings.logo_object_key else None
        )
    return payload


def normalized_text(value):
    return value.strip() if isinstance(value, str) and value.strip() else None


def parse_settings_payload(payload):
    if not isinstance(payload, dict):
        return None, {"request": "JSON body is required."}

    data = {}
    errors = {}
    for field in TEXT_FIELDS:
        if field in payload:
            data[field] = normalized_text(payload[field])

    for field in COLOR_FIELDS:
        if field not in payload:
            continue
        value = normalized_text(payload[field])
        if value is None:
            data[field] = None
        elif not HEX_COLOR.fullmatch(value):
            errors[field] = "Use a six-digit hex color such as #1F6F68."
        else:
            data[field] = value.upper()

    return data, errors


def file_size(file_storage):
    stream = file_storage.stream
    position = stream.tell()
    stream.seek(0, 2)
    size = stream.tell()
    stream.seek(position)
    return size


def valid_svg(stream):
    stream.seek(0)
    content = stream.read()
    stream.seek(0)
    lowered_content = content.lower()
    if b"<!doctype" in lowered_content or b"<!entity" in lowered_content:
        return False
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError:
        return False
    if root.tag.rsplit("}", 1)[-1].lower() != "svg":
        return False
    blocked_tags = {
        "script",
        "style",
        "foreignobject",
        "iframe",
        "object",
        "embed",
    }
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1].lower() in blocked_tags:
            return False
        for name, value in element.attrib.items():
            attribute = name.rsplit("}", 1)[-1].lower()
            normalized_value = value.strip().lower()
            if attribute.startswith("on"):
                return False
            if attribute == "style" and "url(" in normalized_value:
                return False
            if attribute in {"href", "src"} and (
                normalized_value.startswith(("http:", "https:", "//", "javascript:"))
                or normalized_value.startswith("data:")
            ):
                return False
    return True


def logo_content_matches_type(upload):
    upload.stream.seek(0)
    signature = upload.stream.read(8)
    upload.stream.seek(0)
    if upload.mimetype == "image/png":
        return signature == b"\x89PNG\r\n\x1a\n"
    if upload.mimetype == "image/jpeg":
        return signature.startswith(b"\xff\xd8\xff")
    if upload.mimetype == "image/svg+xml":
        return valid_svg(upload.stream)
    return False


def validate_logo_upload():
    upload = request.files.get("file")
    if upload is None or not upload.filename:
        return None, {"file": "This field is required."}

    safe_name = secure_filename(upload.filename)
    extension = f".{safe_name.rsplit('.', 1)[-1].lower()}" if "." in safe_name else ""
    allowed_extensions = ALLOWED_LOGO_TYPES.get(upload.mimetype)
    errors = {}
    if not safe_name or not allowed_extensions or extension not in allowed_extensions:
        errors["file"] = "Use an SVG, PNG, or JPEG logo."
    elif not logo_content_matches_type(upload):
        errors["file"] = "Logo content is invalid or unsafe."

    size = file_size(upload)
    if size <= 0:
        errors["file"] = "The uploaded logo is empty."
    elif size > current_app.config["BRANDING_LOGO_MAX_FILE_SIZE"]:
        max_mb = current_app.config["BRANDING_LOGO_MAX_FILE_SIZE"] // (1024 * 1024)
        errors["file"] = f"Logo size must not exceed {max_mb} MB."

    if errors:
        return None, errors
    upload.stream.seek(0)
    return {
        "upload": upload,
        "file_name": safe_name,
        "file_size": size,
    }, {}


@branding_bp.get("/settings/branding")
@swag_from(branding_get_spec)
def get_branding():
    return success_response(
        settings_response(get_settings()),
        "Branding settings retrieved successfully",
    )


@branding_bp.put("/settings/branding")
@swag_from(branding_update_spec)
def update_branding():
    data, errors = parse_settings_payload(request.get_json(silent=True))
    if errors:
        return error_response("Invalid branding settings", 400, errors)

    settings = get_settings(create=True)
    for field, value in data.items():
        setattr(settings, field, value)
    db.session.commit()
    return success_response(
        settings_response(settings),
        "Branding settings updated successfully",
    )


@branding_bp.post("/settings/branding/logo")
@swag_from(branding_upload_logo_spec)
def upload_branding_logo():
    data, errors = validate_logo_upload()
    if errors:
        return error_response("Invalid branding logo", 400, errors)

    settings = get_settings(create=True)
    previous_key = settings.logo_object_key
    object_key = f"branding/default/logo/{uuid4().hex}_{data['file_name']}"
    storage = get_branding_logo_storage()
    try:
        storage.upload(
            object_key,
            data["upload"].stream,
            data["file_size"],
            data["upload"].mimetype,
        )
        if previous_key:
            storage.delete(previous_key)
    except PrivateObjectStorageError as exc:
        return error_response(str(exc), 502)

    settings.logo_object_key = object_key
    settings.logo_file_name = data["file_name"]
    settings.logo_mime_type = data["upload"].mimetype
    settings.logo_file_size = data["file_size"]
    db.session.commit()
    return success_response(
        settings_response(settings),
        "Branding logo uploaded successfully",
        201,
    )


@branding_bp.delete("/settings/branding/logo")
@swag_from(branding_delete_logo_spec)
def delete_branding_logo():
    settings = get_settings()
    if settings is None or not settings.logo_object_key:
        return success_response(
            resolved_branding(settings),
            "Branding logo already uses the default",
        )

    try:
        get_branding_logo_storage().delete(settings.logo_object_key)
    except PrivateObjectStorageError as exc:
        return error_response(str(exc), 502)

    settings.logo_object_key = None
    settings.logo_file_name = None
    settings.logo_mime_type = None
    settings.logo_file_size = None
    db.session.commit()
    return success_response(
        settings_response(settings),
        "Branding logo deleted successfully",
    )


@branding_bp.get("/public/branding")
@swag_from(branding_public_get_spec)
def get_public_branding():
    return success_response(
        resolved_branding(get_settings()),
        "Public branding retrieved successfully",
    )


@branding_bp.get("/public/branding/logo")
@swag_from(branding_public_logo_spec)
def get_public_branding_logo():
    settings = get_settings()
    if settings is None or not settings.logo_object_key:
        return error_response("Custom branding logo not found", 404)
    try:
        source = get_branding_logo_storage().open(settings.logo_object_key)
    except FileNotFoundError:
        return error_response("Custom branding logo not found", 404)
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

    response = Response(generate(), mimetype=settings.logo_mime_type)
    response.headers["Content-Disposition"] = (
        f'inline; filename="{settings.logo_file_name}"'
    )
    response.headers["Content-Length"] = str(settings.logo_file_size)
    response.headers["Cache-Control"] = "public, max-age=300"
    return response
