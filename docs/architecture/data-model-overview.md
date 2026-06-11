# Data Model Overview

Patient is the central clinical entity.

## Relationships

- A Patient has many Visits.
- A Patient has many Aide Notes, Nurse Notes, Assessments, and Medical Records.
- A Visit belongs to one Patient.
- A Visit has zero or one Aide Note.
- A Visit has zero or one Nurse Note.
- A Visit has zero or many Assessments.
- An Assessment belongs to one Patient and may belong to one Visit.
- OrganizationSettings is currently a singleton independent of clinical data.

## Structured JSON

Aide and Nurse Note checklist/clinical sections and assessment findings use
PostgreSQL JSON columns. This keeps the early form model flexible while still
allowing the UI to render structured sections.

## File Metadata

MedicalRecord stores object key, bucket, file type, size, and uploader metadata.
Patient stores photo metadata directly. OrganizationSettings stores logo
metadata. Their file bytes remain private in MinIO.

## Demo Markers

Clinical tables include `is_demo_data` so deterministic demo records can be
cleared without deleting normal records.

See the [Entity Relationship Diagram](../diagrams/erd.md).
