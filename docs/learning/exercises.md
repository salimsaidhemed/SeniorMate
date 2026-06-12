# SeniorMate Learning Exercises

Use a separate feature branch for each exercise. Update tests, documentation,
and `CHANGELOG.md` when the exercise changes repository behavior.

## Add a New Patient Field

**Goal:** Add a preferred language field end to end.

**Files to inspect**

- `backend/app/models/patient.py`
- `backend/app/routes/patients.py`
- `backend/app/swagger.py`
- `backend/migrations/versions/`
- `frontend/src/views/PatientFormView.js`
- `frontend/src/views/PatientDetailView.js`
- `backend/tests/test_patients.py`

**Suggested steps**

1. Add a nullable model column.
2. Generate and inspect a migration.
3. Add the field to allowed payload fields and serialization.
4. Update OpenAPI.
5. Add create/update tests.
6. Add the form and detail display.

**Expected result:** The field survives create, edit, reload, and API
serialization.

## Add a New Visit Status

**Goal:** Add `missed` as a visit status.

**Files to inspect**

- `backend/app/models/visit.py`
- Visits route validation
- Visits Swagger schemas
- Visit forms, status chips, dashboard/reports
- Visit tests and migration history

**Suggested steps**

1. Update the database check constraint through a migration.
2. Update backend validation and OpenAPI enum.
3. Add the option to frontend forms/filters.
4. Decide how reports count missed visits.
5. Add focused tests.

**Expected result:** Missed visits can be saved, filtered, displayed, and
reported consistently.

## Add a Dashboard Card

**Goal:** Display cancelled visits this month.

**Files to inspect**

- `backend/app/routes/dashboard.py`
- Dashboard Swagger schema
- `backend/tests/test_dashboard.py`
- `frontend/src/services/dashboard.js`
- `frontend/src/views/DashboardView.js`

**Suggested steps**

1. Add the aggregate to the dashboard endpoint.
2. Update Swagger and backend tests.
3. Add the metric card with an appropriate icon and empty value.
4. Build and inspect responsive layout.

**Expected result:** The card reflects seeded/current-month data.

## Add a Report Filter

**Goal:** Filter medical-record summary by `record_type`.

**Files to inspect**

- `backend/app/routes/reports.py`
- Report Swagger specifications
- `frontend/src/services/reports.js`
- `frontend/src/views/ReportDetailView.js`
- `backend/tests/test_reports.py`

**Suggested steps**

1. Parse the new query parameter.
2. Apply it only to the relevant report query.
3. Document the filter.
4. Add frontend filter metadata/control.
5. Test JSON and CSV paths.

**Expected result:** Table, summary, chart groups, and CSV all represent the
same filtered dataset.

## Add a Role Permission

**Goal:** Allow managers, but not nurses, to verify patient photos.

**Files to inspect**

- `backend/app/auth.py`
- `frontend/src/permission-policy.js`
- `frontend/src/permissions.js`
- Auth and permission tests

**Suggested steps**

1. Confirm the desired policy already/does not already exist.
2. Update backend and frontend maps together.
3. Add positive and negative tests.
4. Login with each role and inspect action visibility/API behavior.

**Expected result:** UI visibility and backend enforcement agree.

## Add a New API Endpoint

**Goal:** Add `GET /api/patients/<id>/summary`.

**Files to inspect**

- Patient route and model
- Related visit/note/assessment models
- `backend/app/auth.py`
- `backend/app/swagger.py`
- API tests

**Suggested steps**

1. Define the response and permission.
2. Query only the data needed.
3. Add a route and Swagger spec.
4. Test found/not-found and authorization behavior.
5. Avoid duplicating an existing printable-report payload without reason.

**Expected result:** Swagger and tests describe a stable summary response.

## Add a Frontend Form Field

**Goal:** Add helper text and validation for patient email.

**Files to inspect**

- `PatientFormView.js`
- `services/patients.js`
- Patient backend validation

**Suggested steps**

1. Add local email validation without replacing backend validation.
2. Display a field error near the input.
3. Confirm API errors still map into `errors`.
4. Check create and edit modes.

**Expected result:** Invalid input is clear and valid data saves normally.

## Add a Backend Test

**Goal:** Test that deleting a patient removes related visits.

**Files to inspect**

- `backend/tests/conftest.py`
- `test_patients.py`
- `test_visits.py`
- Patient/Visit relationships

**Suggested steps**

1. Create a patient and visit through the API.
2. Delete the patient.
3. Verify the visit no longer exists.
4. Keep the test independent of execution order.

**Expected result:** The test proves cascade behavior at the application
boundary.

## Debug a Failed Migration

**Goal:** Practice diagnosing a migration revision mismatch.

**Files to inspect**

- `backend/migrations/versions/`
- `backend/migrations/env.py`
- Current model definitions

**Suggested steps**

1. Use a disposable local database.
2. Run `flask db current`, `heads`, and `history`.
3. Identify the expected parent revision.
4. Inspect upgrade/downgrade functions.
5. Restore a clean database and replay upgrades.

**Expected result:** You can explain the mismatch before applying a fix. Do
not practice destructive migration operations on real data.

## Trace an API Request to the Database

**Goal:** Trace patient creation from browser click to SQLAlchemy commit.

**Files to inspect**

- `PatientFormView.js`
- `services/patients.js`
- `services/http.js`
- `backend/app/auth.py`
- `routes/patients.py`
- `models/patient.py`
- `test_patients.py`

**Suggested steps**

1. Add temporary browser/backend breakpoints or safe debug logging locally.
2. Submit a patient.
3. Record payload changes at every boundary.
4. Identify where authorization, validation, serialization, and persistence
   occur.
5. Remove temporary logging.

**Expected result:** You can draw the complete request path and identify the
best layer for a future rule.
