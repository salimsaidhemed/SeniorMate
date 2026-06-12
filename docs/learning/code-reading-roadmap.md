# Code Reading Roadmap

Read SeniorMate in this order to build a mental model from platform boundaries
inward. Do not try to read every file linearly.

## 1. Docker Compose

Read:

- `docker-compose.yml`
- `.env.example`

Questions:

- Which services exist?
- Which addresses are for the host versus containers?
- Which data is persistent?
- Which services must start before the backend?

Outcome: you can draw the local runtime without reading application code.

## 2. Backend Factory and Configuration

Read:

- `backend/run.py`
- `backend/app/__init__.py`
- `backend/app/config.py`
- `backend/app/extensions.py`

Questions:

- How is the Flask app created?
- Where are integrations registered?
- Which endpoints are public?
- How does test configuration replace production configuration?

## 3. Backend Models

Read in this order:

1. `patient.py`
2. `visit.py`
3. `aide_note.py`
4. `nurse_note.py`
5. `patient_assessment.py`
6. `medical_record.py`
7. `organization_settings.py`

Keep the [Data Model Walkthrough](data-model-walkthrough.md) open. Trace foreign
keys, relationship cascades, JSON fields, and `to_dict()` methods.

## 4. Backend Routes

Begin with `routes/patients.py` because it shows CRUD, filtering, validation,
photo storage, and consistent responses.

Then read:

- `visits.py`
- `aide_notes.py`
- `nurse_notes.py`
- `assessments.py`
- `medical_records.py`
- `dashboard.py`
- `reports.py`
- `branding.py`
- `admin_users.py`

For each route, answer:

1. What permission is required?
2. How is input validated?
3. Which records are queried?
4. Where is the transaction committed?
5. What does success/error JSON look like?

## 5. Backend Services and Cross-Cutting Helpers

Read:

- `auth.py`
- `storage.py`
- `keycloak_admin.py`
- `routes/query_utils.py`
- `swagger.py`

Notice which concerns are shared and which remain route-local.

## 6. Frontend Router

Read `frontend/src/router.js`.

Build a list of:

- Route name and path.
- View component.
- Required permission.
- Create/edit/detail/print relationships.

## 7. Frontend Bootstrap and Layout

Read:

- `main.js`
- `views/App.js`
- `branding.js`
- `styles/main.css`

Trace startup ordering, Vuetify defaults, navigation filtering, and the
branding fallback.

## 8. Frontend Services

Read:

- `services/http.js`
- `services/query.js`
- `services/patients.js`
- One JSON-heavy service.
- `services/medicalRecords.js` for multipart/blob handling.

Understand how tokens, JSON, FormData, errors, and downloads differ.

## 9. Frontend Pages

Follow one complete workflow:

1. `PatientListView.js`
2. `PatientFormView.js`
3. `PatientDetailView.js`
4. `MedicalRecordsSection.js`

Then compare the same patterns in Visits and Notes.

## 10. Authentication and RBAC

Read side by side:

- `backend/app/auth.py`
- `frontend/src/auth.js`
- `frontend/src/permission-policy.js`
- `frontend/src/permissions.js`
- `frontend/tests/permissions.test.js`

Look for duplicated policy and the tests that prevent drift.

## 11. Tests

Start at `backend/tests/conftest.py`, then read:

- `test_patients.py`
- `test_auth.py`
- `test_medical_records.py`
- The test matching your intended change.

Ask how external systems are replaced and where database state is reset.

## 12. CI and Delivery

Read:

- `.github/workflows/backend-ci.yml`
- `.github/workflows/frontend-ci.yml`
- `.github/workflows/docker-build.yml`
- `.github/workflows/github-pages.yml`
- Backend and frontend Dockerfiles

Match each CI command to something you can run locally.

## Reading Exercise

Choose one browser action, such as uploading a patient photo. Write down every
file touched from click to database/object storage, then verify your path
against [Request Flows](request-flows.md).
