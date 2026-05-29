# Local Development

SeniorMate is currently in early scaffold form. This guide defines the expected local development workflow as implementation fills in the backend, frontend, and supporting services.

## Prerequisites

- Git
- Python 3.11 or newer
- Node.js 20 or newer
- Docker and Docker Compose

## Environment Setup

Create a local environment file from the safe example:

```bash
cp .env.example .env
```

Do not commit `.env` or any file containing real secrets.

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

When the Flask application is implemented, backend run and test commands should be documented here.

## Frontend Setup

```bash
cd frontend
npm install
```

When the Vue application is implemented, frontend run, build, lint, and test commands should be documented here.

## Docker Setup

```bash
docker compose up --build
```

Use Docker Compose for local service dependencies such as PostgreSQL, Keycloak, and MinIO once those services are defined.

## Validation Before Pull Requests

- Run the relevant backend checks.
- Run the relevant frontend checks.
- Run Docker validation when service definitions change.
- Update `CHANGELOG.md` for notable changes.
