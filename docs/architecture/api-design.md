# API Design

SeniorMate API responses use JSON and keep successful responses in a consistent envelope:

```json
{
  "data": {},
  "message": "Operation completed successfully"
}
```

Validation and not-found responses include a clear message and, when applicable, field-level errors:

```json
{
  "message": "Invalid patient data",
  "errors": {
    "first_name": "This field is required."
  }
}
```

## Interactive API Documentation

SeniorMate exposes browser-based Swagger documentation for local API testing:

- Swagger UI: `http://localhost:5001/api/docs`
- OpenAPI JSON: `http://localhost:5001/api/openapi.json`

Start the local stack with Docker Compose, then open the Swagger UI in a browser to inspect and test the health and patient endpoints.

## Patient API

The Patient API is available under `/api/patients`.

### Patient Fields

- `id`
- `first_name`
- `last_name`
- `date_of_birth`
- `gender`
- `phone`
- `email`
- `address`
- `emergency_contact_name`
- `emergency_contact_phone`
- `diagnosis_summary`
- `status`
- `created_at`
- `updated_at`

`first_name` and `last_name` are required. `status` defaults to `active` and must be either `active` or `inactive`. `date_of_birth` is optional, but when provided it must use `YYYY-MM-DD`.

### List Patients

`GET /api/patients`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "first_name": "Maria",
      "last_name": "Santos",
      "date_of_birth": "1945-03-12",
      "gender": "female",
      "phone": "+1-555-0100",
      "email": "maria.santos@example.com",
      "address": "12 Care Lane",
      "emergency_contact_name": "Ana Santos",
      "emergency_contact_phone": "+1-555-0199",
      "diagnosis_summary": "Requires daily mobility support.",
      "status": "active",
      "created_at": "2026-05-29T10:00:00+00:00",
      "updated_at": "2026-05-29T10:00:00+00:00"
    }
  ],
  "message": "Patients retrieved successfully"
}
```

### Retrieve a Patient

`GET /api/patients/<id>`

Example response:

```json
{
  "data": {
    "id": 1,
    "first_name": "Maria",
    "last_name": "Santos",
    "date_of_birth": "1945-03-12",
    "gender": "female",
    "phone": "+1-555-0100",
    "email": "maria.santos@example.com",
    "address": "12 Care Lane",
    "emergency_contact_name": "Ana Santos",
    "emergency_contact_phone": "+1-555-0199",
    "diagnosis_summary": "Requires daily mobility support.",
    "status": "active",
    "created_at": "2026-05-29T10:00:00+00:00",
    "updated_at": "2026-05-29T10:00:00+00:00"
  },
  "message": "Patient retrieved successfully"
}
```

### Create a Patient

`POST /api/patients`

Example request:

```json
{
  "first_name": "Maria",
  "last_name": "Santos",
  "date_of_birth": "1945-03-12",
  "gender": "female",
  "phone": "+1-555-0100",
  "email": "maria.santos@example.com",
  "address": "12 Care Lane",
  "emergency_contact_name": "Ana Santos",
  "emergency_contact_phone": "+1-555-0199",
  "diagnosis_summary": "Requires daily mobility support."
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "first_name": "Maria",
    "last_name": "Santos",
    "date_of_birth": "1945-03-12",
    "gender": "female",
    "phone": "+1-555-0100",
    "email": "maria.santos@example.com",
    "address": "12 Care Lane",
    "emergency_contact_name": "Ana Santos",
    "emergency_contact_phone": "+1-555-0199",
    "diagnosis_summary": "Requires daily mobility support.",
    "status": "active",
    "created_at": "2026-05-29T10:00:00+00:00",
    "updated_at": "2026-05-29T10:00:00+00:00"
  },
  "message": "Patient created successfully"
}
```

### Update a Patient

`PUT /api/patients/<id>`

Example request:

```json
{
  "phone": "+1-555-0111",
  "status": "inactive"
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "first_name": "Maria",
    "last_name": "Santos",
    "date_of_birth": "1945-03-12",
    "gender": "female",
    "phone": "+1-555-0111",
    "email": "maria.santos@example.com",
    "address": "12 Care Lane",
    "emergency_contact_name": "Ana Santos",
    "emergency_contact_phone": "+1-555-0199",
    "diagnosis_summary": "Requires daily mobility support.",
    "status": "inactive",
    "created_at": "2026-05-29T10:00:00+00:00",
    "updated_at": "2026-05-29T10:05:00+00:00"
  },
  "message": "Patient updated successfully"
}
```

### Delete a Patient

`DELETE /api/patients/<id>`

Example response:

```json
{
  "data": {
    "id": 1
  },
  "message": "Patient deleted successfully"
}
```

## Visit API

The Visit API records caregiver and nursing visits linked to patients.

### Visit Fields

- `id`
- `patient_id`
- `visit_date`
- `visit_type`
- `staff_name`
- `staff_role`
- `time_in`
- `time_out`
- `notes`
- `status`
- `created_at`
- `updated_at`

`patient_id`, `visit_date`, and `visit_type` are required. `visit_date` must use `YYYY-MM-DD`. `staff_role` currently supports `aide` and `nurse`. `status` defaults to `scheduled` and must be `scheduled`, `completed`, or `cancelled`.

### List Visits

`GET /api/visits`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "visit_date": "2026-06-01",
      "visit_type": "Home care visit",
      "staff_name": "Jordan Lee",
      "staff_role": "aide",
      "time_in": "09:00",
      "time_out": "10:30",
      "notes": "Patient completed morning mobility exercises.",
      "status": "scheduled",
      "created_at": "2026-05-31T10:00:00+00:00",
      "updated_at": "2026-05-31T10:00:00+00:00"
    }
  ],
  "message": "Visits retrieved successfully"
}
```

### List Visits for a Patient

`GET /api/patients/<patient_id>/visits`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "visit_date": "2026-06-01",
      "visit_type": "Home care visit",
      "staff_name": "Jordan Lee",
      "staff_role": "aide",
      "time_in": "09:00",
      "time_out": "10:30",
      "notes": "Patient completed morning mobility exercises.",
      "status": "scheduled",
      "created_at": "2026-05-31T10:00:00+00:00",
      "updated_at": "2026-05-31T10:00:00+00:00"
    }
  ],
  "message": "Patient visits retrieved successfully"
}
```

### Retrieve a Visit

`GET /api/visits/<id>`

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_date": "2026-06-01",
    "visit_type": "Home care visit",
    "staff_name": "Jordan Lee",
    "staff_role": "aide",
    "time_in": "09:00",
    "time_out": "10:30",
    "notes": "Patient completed morning mobility exercises.",
    "status": "scheduled",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Visit retrieved successfully"
}
```

### Create a Visit

`POST /api/visits`

Example request:

```json
{
  "patient_id": 1,
  "visit_date": "2026-06-01",
  "visit_type": "Home care visit",
  "staff_name": "Jordan Lee",
  "staff_role": "aide",
  "time_in": "09:00",
  "time_out": "10:30",
  "notes": "Patient completed morning mobility exercises."
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_date": "2026-06-01",
    "visit_type": "Home care visit",
    "staff_name": "Jordan Lee",
    "staff_role": "aide",
    "time_in": "09:00",
    "time_out": "10:30",
    "notes": "Patient completed morning mobility exercises.",
    "status": "scheduled",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Visit created successfully"
}
```

### Update a Visit

`PUT /api/visits/<id>`

Example request:

```json
{
  "staff_role": "nurse",
  "status": "completed",
  "notes": "Vitals checked and medication reminder completed."
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_date": "2026-06-01",
    "visit_type": "Home care visit",
    "staff_name": "Jordan Lee",
    "staff_role": "nurse",
    "time_in": "09:00",
    "time_out": "10:30",
    "notes": "Vitals checked and medication reminder completed.",
    "status": "completed",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:15:00+00:00"
  },
  "message": "Visit updated successfully"
}
```

### Delete a Visit

`DELETE /api/visits/<id>`

Example response:

```json
{
  "data": {
    "id": 1
  },
  "message": "Visit deleted successfully"
}
```

## Aide Note API

The Aide Note API records Home Health Aide visit documentation linked to both a patient and a visit. Checklist sections are stored as JSON for flexibility while the final form structure continues to evolve.

### Aide Note Fields

- `id`
- `patient_id`
- `visit_id`
- `personal_care`
- `nutrition`
- `mental_status`
- `elimination`
- `activity`
- `assistive_devices`
- `housekeeping`
- `additional_notes`
- `aide_name`
- `signature_data`
- `signature_date`
- `time_in`
- `time_out`
- `created_at`
- `updated_at`

`patient_id`, `visit_id`, and `aide_name` are required. `signature_date` is optional, but when provided it must use `YYYY-MM-DD`. The visit must exist and belong to the selected patient. A visit can have only one aide note.

### List Aide Notes

`GET /api/aide-notes`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "visit_id": 1,
      "personal_care": {
        "completed": ["bath", "oral_care"]
      },
      "nutrition": {
        "meal_percentage": 75,
        "fluids_offered": true
      },
      "mental_status": {
        "observed": ["alert", "oriented"]
      },
      "elimination": {
        "voided": true
      },
      "activity": {
        "ambulated": true
      },
      "assistive_devices": {
        "walker": true
      },
      "housekeeping": {
        "completed": ["laundry"]
      },
      "additional_notes": "Patient tolerated care well.",
      "aide_name": "Alex Morgan",
      "signature_data": "data:image/png;base64,...",
      "signature_date": "2026-06-01",
      "time_in": "09:00",
      "time_out": "10:30",
      "created_at": "2026-05-31T10:00:00+00:00",
      "updated_at": "2026-05-31T10:00:00+00:00"
    }
  ],
  "message": "Aide notes retrieved successfully"
}
```

### List Aide Notes for a Patient

`GET /api/patients/<patient_id>/aide-notes`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "visit_id": 1,
      "personal_care": {
        "completed": ["bath", "oral_care"]
      },
      "nutrition": {
        "meal_percentage": 75
      },
      "mental_status": null,
      "elimination": null,
      "activity": null,
      "assistive_devices": null,
      "housekeeping": null,
      "additional_notes": "Patient tolerated care well.",
      "aide_name": "Alex Morgan",
      "signature_data": null,
      "signature_date": "2026-06-01",
      "time_in": "09:00",
      "time_out": "10:30",
      "created_at": "2026-05-31T10:00:00+00:00",
      "updated_at": "2026-05-31T10:00:00+00:00"
    }
  ],
  "message": "Patient aide notes retrieved successfully"
}
```

### Retrieve an Aide Note

`GET /api/aide-notes/<id>`

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "personal_care": {
      "completed": ["bath", "oral_care"]
    },
    "nutrition": {
      "meal_percentage": 75
    },
    "mental_status": null,
    "elimination": null,
    "activity": null,
    "assistive_devices": null,
    "housekeeping": null,
    "additional_notes": "Patient tolerated care well.",
    "aide_name": "Alex Morgan",
    "signature_data": null,
    "signature_date": "2026-06-01",
    "time_in": "09:00",
    "time_out": "10:30",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Aide note retrieved successfully"
}
```

### Retrieve an Aide Note for a Visit

`GET /api/visits/<visit_id>/aide-note`

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "personal_care": {
      "completed": ["bath", "oral_care"]
    },
    "nutrition": {
      "meal_percentage": 75
    },
    "mental_status": null,
    "elimination": null,
    "activity": null,
    "assistive_devices": null,
    "housekeeping": null,
    "additional_notes": "Patient tolerated care well.",
    "aide_name": "Alex Morgan",
    "signature_data": null,
    "signature_date": "2026-06-01",
    "time_in": "09:00",
    "time_out": "10:30",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Visit aide note retrieved successfully"
}
```

### Create an Aide Note

`POST /api/aide-notes`

Example request:

```json
{
  "patient_id": 1,
  "visit_id": 1,
  "personal_care": {
    "completed": ["bath", "oral_care"]
  },
  "nutrition": {
    "meal_percentage": 75,
    "fluids_offered": true
  },
  "mental_status": {
    "observed": ["alert", "oriented"]
  },
  "elimination": {
    "voided": true
  },
  "activity": {
    "ambulated": true
  },
  "assistive_devices": {
    "walker": true
  },
  "housekeeping": {
    "completed": ["laundry"]
  },
  "additional_notes": "Patient tolerated care well.",
  "aide_name": "Alex Morgan",
  "signature_data": "data:image/png;base64,...",
  "signature_date": "2026-06-01",
  "time_in": "09:00",
  "time_out": "10:30"
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "personal_care": {
      "completed": ["bath", "oral_care"]
    },
    "nutrition": {
      "meal_percentage": 75,
      "fluids_offered": true
    },
    "mental_status": {
      "observed": ["alert", "oriented"]
    },
    "elimination": {
      "voided": true
    },
    "activity": {
      "ambulated": true
    },
    "assistive_devices": {
      "walker": true
    },
    "housekeeping": {
      "completed": ["laundry"]
    },
    "additional_notes": "Patient tolerated care well.",
    "aide_name": "Alex Morgan",
    "signature_data": "data:image/png;base64,...",
    "signature_date": "2026-06-01",
    "time_in": "09:00",
    "time_out": "10:30",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Aide note created successfully"
}
```

### Update an Aide Note

`PUT /api/aide-notes/<id>`

Example request:

```json
{
  "aide_name": "Taylor Reed",
  "additional_notes": "Updated after supervisor review."
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "personal_care": {
      "completed": ["bath", "oral_care"]
    },
    "nutrition": {
      "meal_percentage": 75
    },
    "mental_status": null,
    "elimination": null,
    "activity": null,
    "assistive_devices": null,
    "housekeeping": null,
    "additional_notes": "Updated after supervisor review.",
    "aide_name": "Taylor Reed",
    "signature_data": null,
    "signature_date": "2026-06-01",
    "time_in": "09:00",
    "time_out": "10:30",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:10:00+00:00"
  },
  "message": "Aide note updated successfully"
}
```

### Delete an Aide Note

`DELETE /api/aide-notes/<id>`

Example response:

```json
{
  "data": {
    "id": 1
  },
  "message": "Aide note deleted successfully"
}
```
