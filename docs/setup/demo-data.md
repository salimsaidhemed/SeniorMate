# Demo Data

SeniorMate provides CLI-only demo data commands for local presentations and
product evaluation. Demo data is never created automatically and is blocked
unless an operator explicitly enables it.

All generated patients, visits, notes, assessments, and medical records are
fictional. Do not use the demo commands with production data or credentials.

## Enable Demo Commands

Set this local environment value:

```bash
DEMO_DATA_ENABLED=true
```

Recreate the backend container after changing `.env` so it receives the new
value:

```bash
docker compose up -d --force-recreate backend
```

The checked-in default remains `false`.

The commands also refuse to run when `APP_ENV=production`, even if the demo
flag is mistakenly enabled.

The backend container connects to MinIO through
`MINIO_DOCKER_ENDPOINT=http://minio:9000`. `MINIO_ENDPOINT=http://localhost:9000`
is reserved for running the Flask backend directly on the host. If the seeder
reports that private storage is unavailable, recreate the backend container
and confirm the `minio` service is running.

## Prepare the Database

Apply the latest migration before seeding:

```bash
docker compose exec backend flask db upgrade
```

The migration adds an indexed `is_demo_data` marker with a default of `false`
to patients, visits, aide notes, nurse notes, assessments, and medical records.
Normal application records therefore remain non-demo unless explicitly marked.
The marker is included as a read-only field in API responses and Swagger
schemas; normal create and update requests cannot set it.

## Seed Demo Data

```bash
docker compose exec backend flask seed-demo
```

The command creates:

- 24 fictional patient profiles with active and inactive statuses.
- 96 visits spread across the previous 90 days.
- 40 aide notes and 40 nurse notes linked to completed visits.
- 48 fall-risk, nutrition, mobility, cognitive, and general assessments.
- 24 generated fictional care-summary PDFs stored privately in MinIO.

Patient screens use SeniorMate's initials avatar fallback. The seed does not
create synthetic portraits or mark any profile photo as verified.

The data is designed to populate dashboard metrics, charts, recent activity,
patient details, visit details, note views, medical records, assessments, and
printable reports.

## Repeat or Reset

`seed-demo` is repeatable. Before generating a fresh deterministic dataset, it
removes the prior records marked `is_demo_data=true` and their generated MinIO
objects. It does not duplicate the previous dataset.

To remove demo data without recreating it:

```bash
docker compose exec backend flask clear-demo
```

`clear-demo` deletes only explicitly marked demo records. It preserves normal
records. As an additional guard, it refuses to delete demo patients or visits
that have non-demo dependent records attached.

Both commands refuse to run when `DEMO_DATA_ENABLED` is not exactly `true` or
when the application environment is production.

## Demo Users

Clinical demo seeding does not create or modify Keycloak users. The local
Keycloak realm import already provides the development-only accounts described
in [Local Keycloak Setup](keycloak-local-setup.md), including:

- `admin.demo`
- `manager.demo`
- `nurse.demo`
- `caregiver.demo`
- `viewer.demo`

Their placeholder credentials must never be reused outside local development.
Keeping identity setup separate prevents the clinical seed command from
changing realm users unexpectedly.

## Local Python Commands

When running the backend outside Docker:

```bash
cd backend
export FLASK_APP=run.py
export DEMO_DATA_ENABLED=true
flask db upgrade
flask seed-demo
flask clear-demo
```
