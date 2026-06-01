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

List endpoints support simple pagination with `page` and `per_page` query parameters. Paginated responses keep the existing `data` array and add metadata:

```json
{
  "data": [],
  "message": "Records retrieved successfully",
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3
  }
}
```

## Interactive API Documentation

SeniorMate exposes browser-based Swagger documentation for local API testing:

- Swagger UI: `http://localhost:5001/api/docs`
- OpenAPI JSON: `http://localhost:5001/api/openapi.json`

Start the local stack with Docker Compose, then open the Swagger UI in a browser to inspect and test the health and patient endpoints.

## Dashboard API

The Dashboard API summarizes patient, visit, and care-note activity for the frontend dashboard.

### Dashboard Fields

- `total_patients`
- `active_patients`
- `inactive_patients`
- `total_visits`
- `visits_this_month`
- `aide_notes_this_month`
- `nurse_notes_this_month`
- `patients_by_status`
- `patients_by_gender`
- `visits_by_type`
- `visits_by_status`
- `recent_visits`

Grouped chart fields are returned as arrays of `{ "label": "...", "count": 1 }`. The frontend renders these groups with lightweight Vuetify progress bars instead of adding a charting dependency.

### Retrieve Dashboard Stats

`GET /api/dashboard/stats`

Example response:

```json
{
  "data": {
    "total_patients": 2,
    "active_patients": 1,
    "inactive_patients": 1,
    "total_visits": 4,
    "visits_this_month": 3,
    "aide_notes_this_month": 1,
    "nurse_notes_this_month": 1,
    "patients_by_status": [
      {
        "label": "active",
        "count": 1
      },
      {
        "label": "inactive",
        "count": 1
      }
    ],
    "patients_by_gender": [
      {
        "label": "female",
        "count": 1
      },
      {
        "label": "male",
        "count": 1
      }
    ],
    "visits_by_type": [
      {
        "label": "Skilled nursing visit",
        "count": 2
      }
    ],
    "visits_by_status": [
      {
        "label": "completed",
        "count": 3
      }
    ],
    "recent_visits": [
      {
        "id": 4,
        "patient_name": "Maria Santos",
        "visit_date": "2026-06-03",
        "visit_type": "Skilled nursing visit",
        "staff_role": "nurse",
        "status": "completed"
      }
    ]
  },
  "message": "Dashboard stats retrieved successfully"
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

Supported query parameters:

- `search`: matches first name, last name, phone, email, or diagnosis summary
- `status`: filters by `active` or `inactive`
- `gender`: filters by gender value
- `page`
- `per_page`

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

Supported query parameters:

- `search`: matches patient name, staff name, visit type, or notes
- `patient_id`
- `visit_type`
- `staff_role`
- `status`
- `start_date`: filters visits on or after `YYYY-MM-DD`
- `end_date`: filters visits on or before `YYYY-MM-DD`
- `page`
- `per_page`

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

Supported query parameters:

- `patient_id`
- `visit_id`
- `aide_name`: partial match
- `start_date`: filters notes created on or after `YYYY-MM-DD`
- `end_date`: filters notes created on or before `YYYY-MM-DD`
- `page`
- `per_page`

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

## Nurse Note API

The Nurse Note API records clinical nurses progress notes linked to both a patient and a visit. Large clinical assessment sections are stored as JSON for flexibility while the clinical form evolves.

The frontend Nurse Notes UI is available at `http://localhost:5173/nurse-notes` during local development. Visit Detail pages show whether a Nurse Note exists for the visit and provide create, view, and edit actions. The UI groups clinical sections while sending the larger assessment areas as JSON payloads to the API.

### Nurse Note Fields

- `id`
- `patient_id`
- `visit_id`
- `diagnosis`
- `living_arrangements`
- `visit_type`
- `vital_signs`
- `diet`
- `pain_assessment`
- `sensory`
- `neuro`
- `respiratory`
- `cardiac`
- `peripheral_circulation`
- `genitourinary`
- `gastrointestinal`
- `endocrine`
- `skin_integrity`
- `wound_evaluation`
- `mental_status`
- `functional_status`
- `homebound_status`
- `skilled_nursing`
- `response_to_intervention`
- `patient_caregiver_understanding`
- `md_contact`
- `discharge_planning`
- `patient_feedback`
- `narrative`
- `signature_data`
- `signature_date`
- `created_at`
- `updated_at`

`patient_id` and `visit_id` are required. The visit must exist and belong to the selected patient. A visit can have only one nurse note.

### List Nurse Notes

`GET /api/nurse-notes`

Supported query parameters:

- `patient_id`
- `visit_id`
- `diagnosis`: partial match
- `start_date`: filters notes created on or after `YYYY-MM-DD`
- `end_date`: filters notes created on or before `YYYY-MM-DD`
- `page`
- `per_page`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "visit_id": 1,
      "diagnosis": "Hypertension",
      "living_arrangements": {
        "status": "lives with caregiver"
      },
      "visit_type": {
        "type": "routine skilled nursing"
      },
      "vital_signs": {
        "blood_pressure": "120/80",
        "pulse": 72
      },
      "diet": {
        "ordered": "low sodium"
      },
      "pain_assessment": {
        "pain_level": 2
      },
      "sensory": {
        "vision": "glasses"
      },
      "neuro": {
        "orientation": "oriented x3"
      },
      "respiratory": {
        "lungs": "clear"
      },
      "cardiac": {
        "rhythm": "regular"
      },
      "peripheral_circulation": {
        "edema": "none"
      },
      "genitourinary": {
        "voiding": "normal"
      },
      "gastrointestinal": {
        "bowel_sounds": "present"
      },
      "endocrine": {
        "blood_glucose": 110
      },
      "skin_integrity": {
        "intact": true
      },
      "wound_evaluation": {
        "wounds": []
      },
      "mental_status": {
        "mood": "calm"
      },
      "functional_status": {
        "ambulation": "walker"
      },
      "homebound_status": {
        "reason": "requires assistance to leave home"
      },
      "skilled_nursing": "Medication reconciliation completed.",
      "response_to_intervention": "Patient verbalized understanding.",
      "patient_caregiver_understanding": {
        "understood": true
      },
      "md_contact": {
        "contacted": false
      },
      "discharge_planning": "Continue plan of care.",
      "patient_feedback": "Patient reports feeling stable.",
      "narrative": "Skilled nursing visit completed without incident.",
      "signature_data": "data:image/png;base64,...",
      "signature_date": "2026-06-01",
      "created_at": "2026-05-31T10:00:00+00:00",
      "updated_at": "2026-05-31T10:00:00+00:00"
    }
  ],
  "message": "Nurse notes retrieved successfully"
}
```

### List Nurse Notes for a Patient

`GET /api/patients/<patient_id>/nurse-notes`

Example response:

```json
{
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "visit_id": 1,
      "diagnosis": "Hypertension",
      "vital_signs": {
        "blood_pressure": "120/80"
      },
      "skilled_nursing": "Medication reconciliation completed.",
      "narrative": "Skilled nursing visit completed without incident.",
      "created_at": "2026-05-31T10:00:00+00:00",
      "updated_at": "2026-05-31T10:00:00+00:00"
    }
  ],
  "message": "Patient nurse notes retrieved successfully"
}
```

### Retrieve a Nurse Note

`GET /api/nurse-notes/<id>`

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "diagnosis": "Hypertension",
    "vital_signs": {
      "blood_pressure": "120/80",
      "pulse": 72
    },
    "skilled_nursing": "Medication reconciliation completed.",
    "narrative": "Skilled nursing visit completed without incident.",
    "signature_date": "2026-06-01",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Nurse note retrieved successfully"
}
```

### Retrieve a Nurse Note for a Visit

`GET /api/visits/<visit_id>/nurse-note`

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "diagnosis": "Hypertension",
    "vital_signs": {
      "blood_pressure": "120/80"
    },
    "narrative": "Skilled nursing visit completed without incident.",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Visit nurse note retrieved successfully"
}
```

### Create a Nurse Note

`POST /api/nurse-notes`

Example request:

```json
{
  "patient_id": 1,
  "visit_id": 1,
  "diagnosis": "Hypertension",
  "vital_signs": {
    "blood_pressure": "120/80",
    "pulse": 72
  },
  "pain_assessment": {
    "pain_level": 2
  },
  "skilled_nursing": "Medication reconciliation completed.",
  "response_to_intervention": "Patient verbalized understanding.",
  "patient_caregiver_understanding": {
    "understood": true
  },
  "md_contact": {
    "contacted": false
  },
  "discharge_planning": "Continue plan of care.",
  "patient_feedback": "Patient reports feeling stable.",
  "narrative": "Skilled nursing visit completed without incident.",
  "signature_data": "data:image/png;base64,...",
  "signature_date": "2026-06-01"
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "diagnosis": "Hypertension",
    "vital_signs": {
      "blood_pressure": "120/80",
      "pulse": 72
    },
    "pain_assessment": {
      "pain_level": 2
    },
    "skilled_nursing": "Medication reconciliation completed.",
    "response_to_intervention": "Patient verbalized understanding.",
    "patient_caregiver_understanding": {
      "understood": true
    },
    "md_contact": {
      "contacted": false
    },
    "discharge_planning": "Continue plan of care.",
    "patient_feedback": "Patient reports feeling stable.",
    "narrative": "Skilled nursing visit completed without incident.",
    "signature_data": "data:image/png;base64,...",
    "signature_date": "2026-06-01",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:00:00+00:00"
  },
  "message": "Nurse note created successfully"
}
```

### Update a Nurse Note

`PUT /api/nurse-notes/<id>`

Example request:

```json
{
  "diagnosis": "Hypertension and diabetes",
  "narrative": "Updated after nursing review."
}
```

Example response:

```json
{
  "data": {
    "id": 1,
    "patient_id": 1,
    "visit_id": 1,
    "diagnosis": "Hypertension and diabetes",
    "narrative": "Updated after nursing review.",
    "created_at": "2026-05-31T10:00:00+00:00",
    "updated_at": "2026-05-31T10:10:00+00:00"
  },
  "message": "Nurse note updated successfully"
}
```

### Delete a Nurse Note

`DELETE /api/nurse-notes/<id>`

Example response:

```json
{
  "data": {
    "id": 1
  },
  "message": "Nurse note deleted successfully"
}
```
