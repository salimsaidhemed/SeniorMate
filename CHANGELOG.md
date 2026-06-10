# Changelog

All notable changes to SeniorMate will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows semantic versioning once releases begin.

## [Unreleased]

### Fixed

- Fixed Aide Notes and Nurse Notes list routes failing to render and leaving subsequent navigation blank.

### Added

- Added admin-only Keycloak user management with a dedicated Admin API client, user and role endpoints, temporary password resets, Swagger documentation, mocked backend tests, and an Admin → Users interface.
- Added organization branding settings with a singleton database model, private MinIO logo storage, safe public branding delivery, admin/manager APIs, Swagger documentation, dynamic frontend theming, and a Settings → Branding page with live preview and default fallback.
- Added Keycloak/OIDC authentication with local realm configuration, frontend login/logout and token refresh, backend JWT validation, role-based API permissions, protected routes, Swagger bearer authorization, tests, and setup documentation.
- Added authentication, authorization, organization branding, and default product identity design documentation with four original SeniorMate SVG logo concepts.
- Added search, filtering, and pagination for patient, visit, aide note, and nurse note list workflows.
- Added print-friendly patient, visit, aide note, nurse note, and assessment reports with reusable report components and browser print/PDF styling.
- Added patient assessments with optional visit linkage, structured JSON findings, CRUD APIs, Swagger documentation, backend tests, and patient/visit frontend workflows.
- Added private MinIO-backed patient profile photos with upload, preview, verification, deletion, safe API metadata, and initials fallback across patient and visit screens.
- Added patient Medical Records with private MinIO file storage, PostgreSQL metadata, upload/download CRUD APIs, Swagger documentation, tests, and Patient Detail UI integration.
- Added a reusable frontend UI foundation with a SeniorMate Vuetify theme, shared page and feedback components, standardized tables, responsive spacing, and UI guidelines.
- Added the dashboard API and frontend dashboard with patient, visit, care-note, chart, and recent visit activity summaries.
- Added the Nurses Progress Note frontend with visit detail integration, grouped clinical form, read-only detail view, edit workflow, and API service functions.
- Added the Nurses Progress Note API with patient/visit-linked clinical records, JSON clinical section storage, duplicate visit-note prevention, Swagger documentation, tests, and API documentation.
- Added the Home Health Aide Note frontend with visit detail integration, grouped checklist form, read-only detail view, edit workflow, and API service functions.
- Added the Home Health Aide Note API with patient/visit-linked records, JSON checklist storage, duplicate visit-note prevention, Swagger documentation, tests, and API documentation.
- Added the Visits frontend with list, create, edit, detail, delete, API service workflows, and patient detail integration.
- Added the Visits API with patient-linked visit records, migration, CRUD endpoints, Swagger documentation, tests, and API documentation.
- Added the Patient Management frontend with list, create, edit, detail, delete, and API service workflows.
- Added Swagger/OpenAPI documentation with browser-based API testing for health and patient endpoints.
- Added the Patient Management API with database model, migration, CRUD endpoints, validation, tests, and API documentation.
- Prepared GitHub Actions workflows for the Node.js 24 runtime by updating action versions and enabling Node.js 24 compatibility testing.
- Added GitHub Actions CI checks for backend linting/tests, frontend builds, and Docker Compose image builds.
- Added minimal backend pytest coverage for app creation and the `/api/health` endpoint.
- Added a runnable Docker Compose local development stack for Flask, Vue/Vite, PostgreSQL, MinIO, and a future Keycloak profile.
- Added a Flask backend app with environment-based configuration, SQLAlchemy, Flask-Migrate, PostgreSQL support, CORS, and `/api/health`.
- Added a Vue/Vite dashboard that reads the backend API base URL from environment configuration.
- Added repository standardisation documentation for local development, project structure, technology stack, and contribution workflow.
- Added practical issue templates for bug reports and feature requests.
- Added `docs/roadmap.md` to capture near-term product and engineering direction.
- Added `docs/setup/local-development.md` for local setup expectations.
- Added safe placeholder values to `.env.example`.
- Added valid placeholder GitHub Actions workflows for backend, frontend, and Docker validation.

### Changed

- Polished the demo experience with clearer dashboard metrics, reusable detail headers, tabbed patient records, streamlined visit documentation actions, consistent forms and table actions, responsive refinements, and expanded UI guidelines.
- Expanded the pull request template with related task, change type, testing, screenshots, documentation, changelog, and maintainer merge checks.
- Expanded `.gitignore` coverage for Python, Flask, Node/Vue, Docker, editor, environment, and OS-generated files.

## [0.0.0] - 2026-05-29

### Added

- Initial repository setup.
- Maintainer-created project layout for backend, frontend, Docker, and GitHub configuration.
- Initial README describing SeniorMate's purpose, planned features, and intended technology stack.
- Initial contribution guidelines.
- Initial pull request, bug report, and feature request templates.
- Initial `.gitignore` and `CODEOWNERS` configuration.
