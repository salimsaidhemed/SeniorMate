# Local Development

SeniorMate runs locally with Docker Compose. The default stack includes the Flask backend, Vue/Vite frontend, PostgreSQL, and MinIO. Keycloak is documented as an optional future authentication service and is not required for normal local development yet.

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

The default values in `.env.example` are local-only placeholders. Replace them for your machine if ports conflict.

## Docker Compose

Start the local stack:

```bash
docker compose up --build
```

If your machine uses the legacy standalone Compose binary, run `docker-compose up --build` instead.

Stop the stack:

```bash
docker compose down
```

Remove local named volumes when you need a clean database and object store:

```bash
docker compose down -v
```

## Local URLs

- Frontend: `http://localhost:5173`
- Backend health endpoint: `http://localhost:5001/api/health`
- MinIO API: `http://localhost:9000`
- MinIO console: `http://localhost:9001`
- PostgreSQL host connection: `localhost:5432`

Default local PostgreSQL values:

- Database: `seniormate`
- User: `seniormate`
- Password: `change-me-local-only`

Default local MinIO console values:

- User: `local-access-key`
- Password: `change-me-local-only`

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

Run the backend directly from the host when needed:

```bash
flask --app run:app run --debug
```

When running outside Docker, make sure `DATABASE_URL` points to a reachable PostgreSQL instance. Inside Compose, it uses the `postgres` service hostname.

## Frontend Setup

```bash
cd frontend
npm install
```

Run the frontend directly from the host when needed:

```bash
npm run dev
```

Use `VITE_API_BASE_URL` to point the dashboard at the backend API. The default is `http://localhost:5001/api`.

## Docker Setup

```bash
docker compose up --build
```

Docker Compose uses named volumes for persistent local data:

- `postgres_data`
- `minio_data`
- `frontend_node_modules`

## Keycloak

Authentication is not implemented yet. A Keycloak service placeholder is available behind the `auth` profile for future work:

```bash
docker compose --profile auth up keycloak
```

The main app remains usable without login for now.

## Troubleshooting

- If ports are already in use, adjust `BACKEND_PORT`, `FRONTEND_PORT`, `POSTGRES_PORT`, `MINIO_API_PORT`, or `MINIO_CONSOLE_PORT` in `.env`.
- If the backend health endpoint reports `database: unavailable`, wait for PostgreSQL to finish starting or restart the backend container.
- If frontend dependencies behave oddly, rebuild the frontend container with `docker compose build frontend`.
- If local data needs to be reset, run `docker compose down -v`.

## Validation Before Pull Requests

- Run the relevant backend checks.
- Run the relevant frontend checks.
- Run Docker validation when service definitions change.
- Update `CHANGELOG.md` for notable changes.

## CI Checks

Pull requests and pushes to `main` run GitHub Actions checks for:

- Backend linting and pytest coverage.
- Frontend dependency installation and production build.
- Docker Compose configuration and backend/frontend image builds.

The workflows do not require private secrets and do not push Docker images.
