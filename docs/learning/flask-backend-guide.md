# Flask Backend Guide

This guide explains the SeniorMate backend as it exists in v1.0.0.

## Application Factory

[`backend/app/__init__.py`](../../backend/app/__init__.py) exposes
`create_app(config_object=Config)`. The factory pattern lets production code
use `Config` while tests supply `TestConfig`.

The factory initializes:

- Flask and environment configuration.
- CORS.
- Flasgger.
- SQLAlchemy and Flask-Migrate.
- Global API protection.
- Domain blueprints.
- Flask CLI demo commands.
- Public health and root routes.

[`backend/run.py`](../../backend/run.py) creates the application object used by
`flask run`, the development container, and direct Python execution.

## Configuration and Extensions

`app/config.py` reads environment variables once when the class is imported.
Important settings include:

- `SQLALCHEMY_DATABASE_URI`
- `AUTH_ENABLED`
- Keycloak issuer, JWKS, audience, and Admin API values
- MinIO endpoint, credentials, bucket, and secure mode
- File-size limits
- CORS origins

`app/extensions.py` creates unbound `db` and `migrate` objects. The factory
binds them to the current app. This avoids circular imports and makes test apps
possible.

## Blueprints and Routes

Each module under `app/routes/` owns an API area. Blueprints either use a
resource prefix such as `/api/patients` or the shared `/api` prefix.

A typical route module contains:

1. Allowed fields and domain constants.
2. Parsing and validation helpers.
3. Success/error response helpers.
4. CRUD handlers.
5. Related-resource handlers.
6. `@swag_from(...)` references.

Example patient creation:

```text
POST /api/patients
  -> parse_patient_payload()
  -> Patient(**data)
  -> db.session.add()
  -> db.session.commit()
  -> patient.to_dict()
```

## Models and SQLAlchemy

Models live under `app/models/`. They define:

- Table and column mappings.
- Foreign keys and database constraints.
- ORM relationships.
- Timestamp defaults.
- `to_dict()` response serialization.

Important patterns:

- `ondelete="CASCADE"` removes child records with a deleted patient/visit.
- ORM `cascade="all, delete-orphan"` aligns Python-side lifecycle behavior.
- Visit note relationships use `uselist=False` plus a unique `visit_id`.
- Assessment visit deletion uses `SET NULL`, preserving the assessment.
- JSON columns hold flexible checklist and clinical sections.
- check constraints protect statuses, roles, and assessment types.

Models currently serialize themselves. There is no separate serializer layer.

## Runtime Schema and Validation Approach

SeniorMate does **not** currently use Marshmallow or Pydantic.

Runtime validation is implemented with explicit functions such as:

- `parse_patient_payload`
- `parse_aide_note_payload`
- `parse_nurse_note_payload`
- `parse_assessment_payload`
- `validate_upload`

These functions whitelist fields, normalize strings, parse dates/times,
verify relationships, and build field-specific errors.

OpenAPI schemas in `app/swagger.py` document requests and responses, but
Flasgger does not enforce them as the runtime validation layer.

When adding a field, update all relevant layers:

1. Model and migration.
2. Parser/validator.
3. `to_dict()`.
4. Swagger schema.
5. Tests.
6. Frontend form/service if user-facing.

## Migrations

Flask-Migrate integrates Alembic with the app factory. Migration files are
ordered under `backend/migrations/versions/`.

Common commands from `backend/`:

```bash
flask --app run:app db current
flask --app run:app db history
flask --app run:app db migrate -m "Add patient field"
flask --app run:app db upgrade
flask --app run:app db downgrade
```

Always inspect generated migrations. Confirm:

- Correct types and nullability.
- Safe defaults for existing rows.
- Expected constraints and indexes.
- Upgrade and downgrade symmetry.

The container mounts `./backend:/app`, so migration files created inside the
backend container appear in the repository.

## Service Layer

SeniorMate has a selective service layer rather than a universal one.

Extracted adapters:

- `app/storage.py`: private MinIO bucket and object operations.
- `app/keycloak_admin.py`: token caching and Keycloak Admin API operations.

Domain CRUD is mostly performed directly inside route functions. This is
reasonable at the current scale, but a future service layer would be helpful
when:

- The same transaction is reused by multiple interfaces.
- A workflow spans several aggregates.
- Domain rules become difficult to test through routes.
- Retry or audit behavior must be centralized.

Do not create a service class merely to move a few SQLAlchemy calls. Extract
when it creates a clearer boundary.

## Error Handling

Domain routes return consistent JSON errors:

```json
{
  "message": "Invalid aide note data",
  "errors": {
    "visit_id": "Visit does not belong to the selected patient."
  }
}
```

External adapters translate low-level failures:

- MinIO errors become `PrivateObjectStorageError`.
- Keycloak errors become `KeycloakAdminError` with an HTTP-oriented status.
- JWT failures become a generic `401` without exposing token internals.

There is not yet a global Flask exception handler. Unexpected exceptions are
handled by Flask, while expected validation and integration failures are
translated near the route.

## Authentication and Authorization

`app.before_request(protect_api_request)` makes authorization a cross-cutting
API concern.

Public paths include health, Swagger, OpenAPI, and public branding. For other
API requests:

1. `authenticate_request()` reads the bearer token.
2. `decode_access_token()` fetches a signing key through `PyJWKClient`.
3. PyJWT validates signature, issuer, audience, and expiry.
4. Realm and API-client roles are filtered to supported SeniorMate roles.
5. `_required_permission()` maps path and method to a permission.
6. `user_has_permission()` evaluates the role permission union.

`login_required` and `roles_required` decorators are available for special
cases, but most current routes rely on the global hook.

The path-based permission mapper is simple and centralized. When adding a new
route family, update `_resource_for_path()` or the route may be denied because
no permission is resolved.

## Swagger/OpenAPI

Flasgger is initialized in the factory. Specifications are Python dictionaries
in `app/swagger.py` and attached with `@swag_from`.

Development URLs:

- Swagger UI: `http://localhost:5001/api/docs`
- OpenAPI JSON: `http://localhost:5001/api/openapi.json`

When API behavior changes, confirm both the runtime parser and Swagger
description remain aligned.

## Request-to-Response Walkthrough

For `POST /api/patients`:

1. Flask matches the patient blueprint route.
2. `protect_api_request` authenticates and requires `patients.write`.
3. The route reads JSON with `request.get_json(silent=True)`.
4. `parse_patient_payload` validates and normalizes data.
5. A `Patient` object is added to the SQLAlchemy session.
6. `db.session.commit()` persists the transaction.
7. `Patient.to_dict()` converts Python/date fields to JSON-safe values.
8. Flask returns `201` with data and a success message.

For a medical-record upload, the route additionally validates file signatures,
uploads to MinIO, stores metadata, and compensates by deleting the object if
the database commit fails.

## Testing the Backend

`tests/conftest.py` creates:

- A testing Flask app.
- In-memory SQLite tables.
- Authentication-disabled development behavior.
- Fake object storage.
- A fake Keycloak Admin client.

This keeps tests deterministic and fast. Use dependency injection through
`app.extensions` when adding another external adapter.

Run:

```bash
cd backend
.venv/bin/ruff check app tests
.venv/bin/pytest -q
```

Start with the test that matches the route module you changed, then run the
full suite.
