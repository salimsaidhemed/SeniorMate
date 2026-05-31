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

visit_properties = {
    "id": {"type": "integer", "example": 1},
    "patient_id": {"type": "integer", "example": 1},
    "visit_date": {
        "type": "string",
        "format": "date",
        "example": "2026-06-01",
    },
    "visit_type": {"type": "string", "example": "Home care visit"},
    "staff_name": {"type": "string", "nullable": True, "example": "Jordan Lee"},
    "staff_role": {
        "type": "string",
        "nullable": True,
        "enum": ["aide", "nurse"],
        "example": "aide",
    },
    "time_in": {
        "type": "string",
        "nullable": True,
        "example": "09:00",
    },
    "time_out": {
        "type": "string",
        "nullable": True,
        "example": "10:30",
    },
    "notes": {
        "type": "string",
        "nullable": True,
        "example": "Patient completed morning mobility exercises.",
    },
    "status": {
        "type": "string",
        "enum": ["scheduled", "completed", "cancelled"],
        "example": "scheduled",
    },
    "created_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-31T10:00:00+00:00",
    },
    "updated_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-31T10:00:00+00:00",
    },
}

visit_request_properties = {
    key: value
    for key, value in visit_properties.items()
    if key not in {"id", "created_at", "updated_at"}
}

checklist_schema = {
    "type": "object",
    "nullable": True,
    "additionalProperties": True,
    "example": {"completed": ["bath", "oral_care"], "declined": []},
}

aide_note_properties = {
    "id": {"type": "integer", "example": 1},
    "patient_id": {"type": "integer", "example": 1},
    "visit_id": {"type": "integer", "example": 1},
    "personal_care": checklist_schema,
    "nutrition": checklist_schema,
    "mental_status": checklist_schema,
    "elimination": checklist_schema,
    "activity": checklist_schema,
    "assistive_devices": checklist_schema,
    "housekeeping": checklist_schema,
    "additional_notes": {
        "type": "string",
        "nullable": True,
        "example": "Patient tolerated care well.",
    },
    "aide_name": {"type": "string", "example": "Alex Morgan"},
    "signature_data": {
        "type": "string",
        "nullable": True,
        "example": "data:image/png;base64,...",
    },
    "signature_date": {
        "type": "string",
        "format": "date",
        "nullable": True,
        "example": "2026-06-01",
    },
    "time_in": {"type": "string", "nullable": True, "example": "09:00"},
    "time_out": {"type": "string", "nullable": True, "example": "10:30"},
    "created_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-31T10:00:00+00:00",
    },
    "updated_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-31T10:00:00+00:00",
    },
}

aide_note_request_properties = {
    key: value
    for key, value in aide_note_properties.items()
    if key not in {"id", "created_at", "updated_at"}
}

clinical_section_schema = {
    "type": "object",
    "nullable": True,
    "additionalProperties": True,
    "example": {"findings": ["within normal limits"], "comments": "Stable"},
}

nurse_note_properties = {
    "id": {"type": "integer", "example": 1},
    "patient_id": {"type": "integer", "example": 1},
    "visit_id": {"type": "integer", "example": 1},
    "diagnosis": {"type": "string", "nullable": True, "example": "Hypertension"},
    "living_arrangements": clinical_section_schema,
    "visit_type": clinical_section_schema,
    "vital_signs": clinical_section_schema,
    "diet": clinical_section_schema,
    "pain_assessment": clinical_section_schema,
    "sensory": clinical_section_schema,
    "neuro": clinical_section_schema,
    "respiratory": clinical_section_schema,
    "cardiac": clinical_section_schema,
    "peripheral_circulation": clinical_section_schema,
    "genitourinary": clinical_section_schema,
    "gastrointestinal": clinical_section_schema,
    "endocrine": clinical_section_schema,
    "skin_integrity": clinical_section_schema,
    "wound_evaluation": clinical_section_schema,
    "mental_status": clinical_section_schema,
    "functional_status": clinical_section_schema,
    "homebound_status": clinical_section_schema,
    "skilled_nursing": {
        "type": "string",
        "nullable": True,
        "example": "Medication reconciliation completed.",
    },
    "response_to_intervention": {
        "type": "string",
        "nullable": True,
        "example": "Patient verbalized improvement after education.",
    },
    "patient_caregiver_understanding": clinical_section_schema,
    "md_contact": clinical_section_schema,
    "discharge_planning": {
        "type": "string",
        "nullable": True,
        "example": "Continue current plan of care.",
    },
    "patient_feedback": {
        "type": "string",
        "nullable": True,
        "example": "Patient reports feeling safer at home.",
    },
    "narrative": {
        "type": "string",
        "nullable": True,
        "example": "Skilled nursing visit completed without incident.",
    },
    "signature_data": {
        "type": "string",
        "nullable": True,
        "example": "data:image/png;base64,...",
    },
    "signature_date": {
        "type": "string",
        "format": "date",
        "nullable": True,
        "example": "2026-06-01",
    },
    "created_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-31T10:00:00+00:00",
    },
    "updated_at": {
        "type": "string",
        "format": "date-time",
        "example": "2026-05-31T10:00:00+00:00",
    },
}

nurse_note_request_properties = {
    key: value
    for key, value in nurse_note_properties.items()
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
        "Visit": {
            "type": "object",
            "properties": visit_properties,
        },
        "VisitCreate": {
            "type": "object",
            "required": ["patient_id", "visit_date", "visit_type"],
            "properties": visit_request_properties,
        },
        "VisitUpdate": {
            "type": "object",
            "properties": visit_request_properties,
        },
        "AideNote": {
            "type": "object",
            "properties": aide_note_properties,
        },
        "AideNoteCreate": {
            "type": "object",
            "required": ["patient_id", "visit_id", "aide_name"],
            "properties": aide_note_request_properties,
        },
        "AideNoteUpdate": {
            "type": "object",
            "properties": aide_note_request_properties,
        },
        "NurseNote": {
            "type": "object",
            "properties": nurse_note_properties,
        },
        "NurseNoteCreate": {
            "type": "object",
            "required": ["patient_id", "visit_id"],
            "properties": nurse_note_request_properties,
        },
        "NurseNoteUpdate": {
            "type": "object",
            "properties": nurse_note_request_properties,
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
        "VisitResponse": {
            "type": "object",
            "properties": {
                "data": {"$ref": "#/definitions/Visit"},
                "message": {
                    "type": "string",
                    "example": "Visit retrieved successfully",
                },
            },
        },
        "VisitListResponse": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Visit"},
                },
                "message": {
                    "type": "string",
                    "example": "Visits retrieved successfully",
                },
            },
        },
        "AideNoteResponse": {
            "type": "object",
            "properties": {
                "data": {"$ref": "#/definitions/AideNote"},
                "message": {
                    "type": "string",
                    "example": "Aide note retrieved successfully",
                },
            },
        },
        "AideNoteListResponse": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/AideNote"},
                },
                "message": {
                    "type": "string",
                    "example": "Aide notes retrieved successfully",
                },
            },
        },
        "NurseNoteResponse": {
            "type": "object",
            "properties": {
                "data": {"$ref": "#/definitions/NurseNote"},
                "message": {
                    "type": "string",
                    "example": "Nurse note retrieved successfully",
                },
            },
        },
        "NurseNoteListResponse": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/NurseNote"},
                },
                "message": {
                    "type": "string",
                    "example": "Nurse notes retrieved successfully",
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

visit_list_spec = {
    "tags": ["Visits"],
    "summary": "List visits",
    "responses": {
        200: {
            "description": "Visits retrieved successfully.",
            "schema": {"$ref": "#/definitions/VisitListResponse"},
        }
    },
}

visit_get_spec = {
    "tags": ["Visits"],
    "summary": "Retrieve a visit",
    "parameters": [
        {
            "name": "visit_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Visit retrieved successfully.",
            "schema": {"$ref": "#/definitions/VisitResponse"},
        },
        404: {
            "description": "Visit not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

visit_create_spec = {
    "tags": ["Visits"],
    "summary": "Create a visit",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/VisitCreate"},
        }
    ],
    "responses": {
        201: {
            "description": "Visit created successfully.",
            "schema": {"$ref": "#/definitions/VisitResponse"},
        },
        400: {
            "description": "Invalid visit data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

visit_update_spec = {
    "tags": ["Visits"],
    "summary": "Update a visit",
    "parameters": [
        {
            "name": "visit_id",
            "in": "path",
            "type": "integer",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/VisitUpdate"},
        },
    ],
    "responses": {
        200: {
            "description": "Visit updated successfully.",
            "schema": {"$ref": "#/definitions/VisitResponse"},
        },
        400: {
            "description": "Invalid visit data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
        404: {
            "description": "Visit not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

visit_delete_spec = {
    "tags": ["Visits"],
    "summary": "Delete a visit",
    "parameters": [
        {
            "name": "visit_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Visit deleted successfully.",
            "schema": {"$ref": "#/definitions/DeleteSuccessResponse"},
        },
        404: {
            "description": "Visit not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

patient_visits_list_spec = {
    "tags": ["Visits"],
    "summary": "List visits for a patient",
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
            "description": "Patient visits retrieved successfully.",
            "schema": {"$ref": "#/definitions/VisitListResponse"},
        },
        404: {
            "description": "Patient not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

aide_note_list_spec = {
    "tags": ["Aide Notes"],
    "summary": "List aide notes",
    "responses": {
        200: {
            "description": "Aide notes retrieved successfully.",
            "schema": {"$ref": "#/definitions/AideNoteListResponse"},
        }
    },
}

aide_note_get_spec = {
    "tags": ["Aide Notes"],
    "summary": "Retrieve an aide note",
    "parameters": [
        {
            "name": "aide_note_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Aide note retrieved successfully.",
            "schema": {"$ref": "#/definitions/AideNoteResponse"},
        },
        404: {
            "description": "Aide note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

aide_note_create_spec = {
    "tags": ["Aide Notes"],
    "summary": "Create an aide note",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/AideNoteCreate"},
        }
    ],
    "responses": {
        201: {
            "description": "Aide note created successfully.",
            "schema": {"$ref": "#/definitions/AideNoteResponse"},
        },
        400: {
            "description": "Invalid aide note data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

aide_note_update_spec = {
    "tags": ["Aide Notes"],
    "summary": "Update an aide note",
    "parameters": [
        {
            "name": "aide_note_id",
            "in": "path",
            "type": "integer",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/AideNoteUpdate"},
        },
    ],
    "responses": {
        200: {
            "description": "Aide note updated successfully.",
            "schema": {"$ref": "#/definitions/AideNoteResponse"},
        },
        400: {
            "description": "Invalid aide note data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
        404: {
            "description": "Aide note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

aide_note_delete_spec = {
    "tags": ["Aide Notes"],
    "summary": "Delete an aide note",
    "parameters": [
        {
            "name": "aide_note_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Aide note deleted successfully.",
            "schema": {"$ref": "#/definitions/DeleteSuccessResponse"},
        },
        404: {
            "description": "Aide note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

patient_aide_notes_list_spec = {
    "tags": ["Aide Notes"],
    "summary": "List aide notes for a patient",
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
            "description": "Patient aide notes retrieved successfully.",
            "schema": {"$ref": "#/definitions/AideNoteListResponse"},
        },
        404: {
            "description": "Patient not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

visit_aide_note_get_spec = {
    "tags": ["Aide Notes"],
    "summary": "Retrieve the aide note for a visit",
    "parameters": [
        {
            "name": "visit_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Visit aide note retrieved successfully.",
            "schema": {"$ref": "#/definitions/AideNoteResponse"},
        },
        404: {
            "description": "Visit or aide note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

nurse_note_list_spec = {
    "tags": ["Nurse Notes"],
    "summary": "List nurse notes",
    "responses": {
        200: {
            "description": "Nurse notes retrieved successfully.",
            "schema": {"$ref": "#/definitions/NurseNoteListResponse"},
        }
    },
}

nurse_note_get_spec = {
    "tags": ["Nurse Notes"],
    "summary": "Retrieve a nurse note",
    "parameters": [
        {
            "name": "nurse_note_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Nurse note retrieved successfully.",
            "schema": {"$ref": "#/definitions/NurseNoteResponse"},
        },
        404: {
            "description": "Nurse note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

nurse_note_create_spec = {
    "tags": ["Nurse Notes"],
    "summary": "Create a nurse note",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/NurseNoteCreate"},
        }
    ],
    "responses": {
        201: {
            "description": "Nurse note created successfully.",
            "schema": {"$ref": "#/definitions/NurseNoteResponse"},
        },
        400: {
            "description": "Invalid nurse note data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

nurse_note_update_spec = {
    "tags": ["Nurse Notes"],
    "summary": "Update a nurse note",
    "parameters": [
        {
            "name": "nurse_note_id",
            "in": "path",
            "type": "integer",
            "required": True,
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {"$ref": "#/definitions/NurseNoteUpdate"},
        },
    ],
    "responses": {
        200: {
            "description": "Nurse note updated successfully.",
            "schema": {"$ref": "#/definitions/NurseNoteResponse"},
        },
        400: {
            "description": "Invalid nurse note data.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
        404: {
            "description": "Nurse note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

nurse_note_delete_spec = {
    "tags": ["Nurse Notes"],
    "summary": "Delete a nurse note",
    "parameters": [
        {
            "name": "nurse_note_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Nurse note deleted successfully.",
            "schema": {"$ref": "#/definitions/DeleteSuccessResponse"},
        },
        404: {
            "description": "Nurse note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

patient_nurse_notes_list_spec = {
    "tags": ["Nurse Notes"],
    "summary": "List nurse notes for a patient",
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
            "description": "Patient nurse notes retrieved successfully.",
            "schema": {"$ref": "#/definitions/NurseNoteListResponse"},
        },
        404: {
            "description": "Patient not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}

visit_nurse_note_get_spec = {
    "tags": ["Nurse Notes"],
    "summary": "Retrieve the nurse note for a visit",
    "parameters": [
        {
            "name": "visit_id",
            "in": "path",
            "type": "integer",
            "required": True,
        }
    ],
    "responses": {
        200: {
            "description": "Visit nurse note retrieved successfully.",
            "schema": {"$ref": "#/definitions/NurseNoteResponse"},
        },
        404: {
            "description": "Visit or nurse note not found.",
            "schema": {"$ref": "#/definitions/ErrorResponse"},
        },
    },
}
