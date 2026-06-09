# Changelog

All notable changes to SeniorMate will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows semantic versioning once releases begin.

## [Unreleased]

### Added

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
