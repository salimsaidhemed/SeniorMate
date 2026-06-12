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

**Read first**

- [SQLAlchemy mapped classes](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)
- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Vue form bindings](https://vuejs.org/guide/essentials/forms.html)
- [Vuetify text fields](https://vuetifyjs.com/en/components/text-fields/)

**Suggested steps**

1. Add a nullable model column.
2. Generate and inspect a migration.
3. Add the field to allowed payload fields and serialization.
4. Update OpenAPI.
5. Add create/update tests.
6. Add the form and detail display.

**Expected result:** The field survives create, edit, reload, and API
serialization.

**Expected skills learned**

- Database model and migration changes
- Backend serialization and validation
- OpenAPI schema maintenance
- Vue and Vuetify form changes
- End-to-end regression testing

## Add a New Visit Status

**Goal:** Add `missed` as a visit status.

**Files to inspect**

- `backend/app/models/visit.py`
- Visits route validation
- Visits Swagger schemas
- Visit forms, status chips, dashboard/reports
- Visit tests and migration history

**Read first**

- [PostgreSQL check constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Alembic operations reference](https://alembic.sqlalchemy.org/en/latest/ops.html)
- [Vue conditional rendering](https://vuejs.org/guide/essentials/conditional.html)
- [Vuetify chips](https://vuetifyjs.com/en/components/chips/)

**Suggested steps**

1. Update the database check constraint through a migration.
2. Update backend validation and OpenAPI enum.
3. Add the option to frontend forms/filters.
4. Decide how reports count missed visits.
5. Add focused tests.

**Expected result:** Missed visits can be saved, filtered, displayed, and
reported consistently.

**Expected skills learned**

- Constraint evolution through migrations
- Keeping backend enums and frontend options aligned
- Updating aggregates and reports safely
- Testing a value across persistence, API, and UI layers

## Add a Dashboard Card

**Goal:** Display cancelled visits this month.

**Files to inspect**

- `backend/app/routes/dashboard.py`
- Dashboard Swagger schema
- `backend/tests/test_dashboard.py`
- `frontend/src/services/dashboard.js`
- `frontend/src/views/DashboardView.js`

**Read first**

- [SQLAlchemy query guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
- [Vue computed properties](https://vuejs.org/guide/essentials/computed.html)
- [Vuetify cards](https://vuetifyjs.com/en/components/cards/)
- [Vuetify grid system](https://vuetifyjs.com/en/components/grids/)

**Suggested steps**

1. Add the aggregate to the dashboard endpoint.
2. Update Swagger and backend tests.
3. Add the metric card with an appropriate icon and empty value.
4. Build and inspect responsive layout.

**Expected result:** The card reflects seeded/current-month data.

**Expected skills learned**

- Aggregate database queries
- API response evolution
- Reactive dashboard rendering
- Responsive Vuetify layout

## Add a Report Filter

**Goal:** Filter medical-record summary by `record_type`.

**Files to inspect**

- `backend/app/routes/reports.py`
- Report Swagger specifications
- `frontend/src/services/reports.js`
- `frontend/src/views/ReportDetailView.js`
- `backend/tests/test_reports.py`

**Read first**

- [Flask request data](https://flask.palletsprojects.com/en/stable/api/#flask.Request)
- [SQLAlchemy SELECT and WHERE](https://docs.sqlalchemy.org/en/20/tutorial/data_select.html)
- [OpenAPI parameters](https://swagger.io/docs/specification/v3_0/describing-parameters/)
- [Vue form bindings](https://vuejs.org/guide/essentials/forms.html)

**Suggested steps**

1. Parse the new query parameter.
2. Apply it only to the relevant report query.
3. Document the filter.
4. Add frontend filter metadata/control.
5. Test JSON and CSV paths.

**Expected result:** Table, summary, chart groups, and CSV all represent the
same filtered dataset.

**Expected skills learned**

- Query parameter parsing
- Composable database filters
- JSON and CSV response consistency
- Filter state in a frontend view

## Add a Role Permission

**Goal:** Allow managers, but not nurses, to verify patient photos.

**Files to inspect**

- `backend/app/auth.py`
- `frontend/src/permission-policy.js`
- `frontend/src/permissions.js`
- Auth and permission tests

**Read first**

- [Keycloak role mappings](https://www.keycloak.org/docs/latest/server_admin/#role-mappings)
- [Vue Router route meta fields](https://router.vuejs.org/guide/advanced/meta.html)
- [JWT introduction](https://jwt.io/introduction)
- [SeniorMate roles and permissions](../user-guide/roles-and-permissions.md)

**Suggested steps**

1. Confirm the desired policy already/does not already exist.
2. Update backend and frontend maps together.
3. Add positive and negative tests.
4. Login with each role and inspect action visibility/API behavior.

**Expected result:** UI visibility and backend enforcement agree.

**Expected skills learned**

- Role-based access control design
- Backend authorization enforcement
- Frontend permission-driven UX
- Positive and negative permission testing

## Add a New API Endpoint

**Goal:** Add `GET /api/patients/<id>/summary`.

**Files to inspect**

- Patient route and model
- Related visit/note/assessment models
- `backend/app/auth.py`
- `backend/app/swagger.py`
- API tests

**Read first**

- [Flask routing](https://flask.palletsprojects.com/en/stable/quickstart/#routing)
- [SQLAlchemy relationship loading](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
- [OpenAPI paths and operations](https://swagger.io/docs/specification/v3_0/paths-and-operations/)
- [Flask testing](https://flask.palletsprojects.com/en/stable/testing/)

**Suggested steps**

1. Define the response and permission.
2. Query only the data needed.
3. Add a route and Swagger spec.
4. Test found/not-found and authorization behavior.
5. Avoid duplicating an existing printable-report payload without reason.

**Expected result:** Swagger and tests describe a stable summary response.

**Expected skills learned**

- REST endpoint design
- Querying related domain data
- Authorization and error handling
- OpenAPI documentation and API testing

## Add a Frontend Form Field

**Goal:** Add helper text and validation for patient email.

**Files to inspect**

- `PatientFormView.js`
- `services/patients.js`
- Patient backend validation

**Read first**

- [Vue form bindings](https://vuejs.org/guide/essentials/forms.html)
- [Vue event handling](https://vuejs.org/guide/essentials/event-handling.html)
- [Vuetify forms](https://vuetifyjs.com/en/components/forms/)
- [Vuetify text fields](https://vuetifyjs.com/en/components/text-fields/)

**Suggested steps**

1. Add local email validation without replacing backend validation.
2. Display a field error near the input.
3. Confirm API errors still map into `errors`.
4. Check create and edit modes.

**Expected result:** Invalid input is clear and valid data saves normally.

**Expected skills learned**

- Reactive form state
- Client-side validation and helper text
- Mapping backend errors into UI feedback
- Testing create and edit behavior

## Add a Backend Test

**Goal:** Test that deleting a patient removes related visits.

**Files to inspect**

- `backend/tests/conftest.py`
- `test_patients.py`
- `test_visits.py`
- Patient/Visit relationships

**Read first**

- [Pytest documentation](https://docs.pytest.org/en/stable/)
- [Flask testing](https://flask.palletsprojects.com/en/stable/testing/)
- [SQLAlchemy cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html)

**Suggested steps**

1. Create a patient and visit through the API.
2. Delete the patient.
3. Verify the visit no longer exists.
4. Keep the test independent of execution order.

**Expected result:** The test proves cascade behavior at the application
boundary.

**Expected skills learned**

- Test fixture usage
- Arrange, act, assert structure
- Relationship cascade behavior
- Isolated API-level regression testing

## Debug a Failed Migration

**Goal:** Practice diagnosing a migration revision mismatch.

**Files to inspect**

- `backend/migrations/versions/`
- `backend/migrations/env.py`
- Current model definitions

**Read first**

- [Flask-Migrate documentation](https://flask-migrate.readthedocs.io/)
- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic branches](https://alembic.sqlalchemy.org/en/latest/branches.html)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)

**Suggested steps**

1. Use a disposable local database.
2. Run `flask db current`, `heads`, and `history`.
3. Identify the expected parent revision.
4. Inspect upgrade/downgrade functions.
5. Restore a clean database and replay upgrades.

**Expected result:** You can explain the mismatch before applying a fix. Do
not practice destructive migration operations on real data.

**Expected skills learned**

- Reading a migration graph
- Diagnosing revision and head mismatches
- Replaying migrations against disposable data
- Separating diagnosis from destructive repair

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

**Read first**

- [MDN HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [Flask request context](https://flask.palletsprojects.com/en/stable/reqcontext/)
- [SQLAlchemy session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)

**Suggested steps**

1. Add temporary browser/backend breakpoints or safe debug logging locally.
2. Submit a patient.
3. Record payload changes at every boundary.
4. Identify where authorization, validation, serialization, and persistence
   occur.
5. Remove temporary logging.

**Expected result:** You can draw the complete request path and identify the
best layer for a future rule.

**Expected skills learned**

- Browser-to-database request tracing
- Identifying authentication and validation boundaries
- Understanding SQLAlchemy session and commit behavior
- Choosing the correct layer for a change
