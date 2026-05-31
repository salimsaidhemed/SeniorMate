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
