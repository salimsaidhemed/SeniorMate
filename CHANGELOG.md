# Changelog

All notable changes to SeniorMate will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows semantic versioning once releases begin.

## [Unreleased]

### Added

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
