# Database Overview

SeniorMate uses PostgreSQL through SQLAlchemy and Flask-Migrate.

## Domain Tables

- `patients`
- `visits`
- `aide_notes`
- `nurse_notes`
- `patient_assessments`
- `medical_records`
- `organization_settings`

Patient is the primary clinical aggregate. Visits, notes, assessments, and
medical-record metadata reference a patient. Aide and Nurse Notes are each
unique per visit. Assessments may optionally reference a visit.

File bytes are not stored in PostgreSQL. Medical record, patient photo, and
branding logo metadata reference private MinIO objects.

## Migrations

```bash
docker compose exec backend flask db upgrade
docker compose exec backend flask db current
```

Create migrations only after reviewing model and constraint changes. Back up
production data before applying a migration.

See the [ERD](../diagrams/erd.md) and
[Data Model Overview](../architecture/data-model-overview.md).
