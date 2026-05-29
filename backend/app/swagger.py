patient_properties = {
    "id": {"type": "integer", "example": 1},
    "first_name": {"type": "string", "example": "Maria"},
    "last_name": {"type": "string", "example": "Santos"},
    "date_of_birth": {
        "type": "string",
        "format": "date",
        "nullable": True,
        "example": "1945-03-12",
    },
    "gender": {"type": "string", "nullable": True, "example": "female"},
    "phone": {"type": "string", "nullable": True, "example": "+1-555-0100"},
    "email": {
        "type": "string",
        "format": "email",
        "nullable": True,
        "example": "maria.santos@example.com",
    },
    "address": {"type": "string", "nullable": True, "example": "12 Care Lane"},
    "emergency_contact_name": {
        "type": "string",
        "nullable": True,
        "example": "Ana Santos",
    },
    "emergency_contact_phone": {
        "type": "string",
        "nullable": True,
        "example": "+1-555-0199",
    },
    "diagnosis_summary": {
        "type": "string",
        "nullable": True,
        "example": "Requires daily mobility support.",
    },
    "status": {
        "type": "string",
        "enum": ["active", "inactive"],
        "example": "active",
    },
    "created_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-29T10:00:00+00:00",
    },
    "updated_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-29T10:00:00+00:00",
    },
}

patient_request_properties = {
    key: value
    for key, value in patient_properties.items()
    if key not in {"id", "created_at", "updated_at"}
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "openapi",
            "route": "/api/openapi.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "SeniorMate API",
        "description": "Interactive API documentation for SeniorMate.",
        "version": "0.1.0",
    },
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "definitions": {
        "Patient": {
            "type": "object",
            "properties": patient_properties,
        },
        "PatientCreate": {
            "type": "object",
            "required": ["first_name", "last_name"],
            "properties": patient_request_properties,
        },
        "PatientUpdate": {
            "type": "object",
            "properties": patient_request_properties,
        },
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "Invalid patient data",
                },
                "errors": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "example": {"first_name": "This field is required."},
                },
            },
        },
        "PatientSuccessResponse": {
            "type": "object",
            "properties": {
                "data": {"$ref": "#/definitions/Patient"},
                "message": {
                    "type": "string",
                    "example": "Patient retrieved successfully",
                },
            },
        },
        "PatientListSuccessResponse": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Patient"},
                },
                "message": {
                    "type": "string",
                    "example": "Patients retrieved successfully",
                },
            },
        },
        "DeleteSuccessResponse": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {"id": {"type": "integer", "example": 1}},
                },
                "message": {
                    "type": "string",
                    "example": "Patient deleted successfully",
                },
            },
        },
    },
}

health_spec = {
    "tags": ["Health"],
    "summary": "Check backend and database health",
    "responses": {
        200: {
            "description": "Backend and database are available.",
            "schema": {
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "example": "seniormate-backend",
                    },
                    "status": {"type": "string", "example": "ok"},
                    "database": {"type": "string", "example": "ok"},
                    "minio_endpoint": {
                        "type": "string",
                        "example": "http://minio:9000",
                    },
                },
            },
        },
        503: {
            "description": "Backend is reachable but a dependency is unavailable.",
        },
    },
}

patient_list_spec = {
    "tags": ["Patients"],
    "summary": "List patients",
    "responses": {
        200: {
            "description": "Patients retrieved successfully.",
            "schema": {"$ref": "#/definitions/PatientListSuccessResponse"},
        }
    },
}

patient_get_spec = {
    "tags": ["Patients"],
    "summary": "Retrieve a patient",
    "parameters": [
        {
            "name": "patient_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Patient retrieved successfully.",
            "schema": {"$ref": "#/definitions/PatientSuccessResponse"},
        },
        404: {
            "description": "Patient not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

patient_create_spec = {
    "tags": ["Patients"],
    "summary": "Create a patient",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/PatientCreate"},
        }
    ],
    "responses": {
        201: {
            "description": "Patient created successfully.",
            "schema": {"$ref": "#/definitions/PatientSuccessResponse"},
        },
        400: {
            "description": "Invalid patient data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

patient_update_spec = {
    "tags": ["Patients"],
    "summary": "Update a patient",
    "parameters": [
        {
            "name": "patient_id",
            "in": "path",
            "type": "integer",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/PatientUpdate"},
        },
    ],
    "responses": {
        200: {
            "description": "Patient updated successfully.",
            "schema": {"$ref": "#/definitions/PatientSuccessResponse"},
        },
        400: {
            "description": "Invalid patient data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
        404: {
            "description": "Patient not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

patient_delete_spec = {
    "tags": ["Patients"],
    "summary": "Delete a patient",
    "parameters": [
        {
            "name": "patient_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Patient deleted successfully.",
            "schema": {"$ref": "#/definitions/DeleteSuccessResponse"},
        },
        404: {
            "description": "Patient not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}
