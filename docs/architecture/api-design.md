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
