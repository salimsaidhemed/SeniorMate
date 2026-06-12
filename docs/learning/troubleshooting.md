# SeniorMate Troubleshooting Guide

Use this guide to move from a symptom to the failing boundary. Run commands
from the repository root unless noted otherwise.

## Baseline Checks

```bash
docker compose ps
docker compose config
docker compose logs --tail=100 backend frontend postgres minio keycloak
curl http://localhost:5001/api/health
```

Do not paste secrets or access tokens into issues or pull requests.

## Backend Does Not Start

**Symptoms**

- Frontend shows `Failed to fetch`.
- Backend container restarts.
- Flask reports an import error.

**Likely causes**

- Missing Python dependency.
- Invalid environment value.
- Database unavailable.
- Import or syntax error.

**Inspect**

- `backend/requirements.txt`
- `backend/app/__init__.py`
- `backend/app/config.py`
- `backend/run.py`
- `docker-compose.yml`

**Commands**

```bash
docker compose logs --tail=200 backend
docker compose build --no-cache backend
docker compose run --rm backend python -m pip check
cd backend && .venv/bin/pytest -q
```

**Suggested fix**

Add the missing dependency to requirements, correct the environment value, or
fix the import. Rebuild the image after dependency changes.

## Frontend Cannot Reach Backend

**Symptoms**

- Browser displays `Failed to fetch`.
- Network request targets the wrong port.
- Backend logs show no request.

**Likely causes**

- Incorrect `VITE_API_BASE_URL`.
- Backend is stopped.
- CORS origin mismatch.
- Browser is using a stale Vite build/configuration.

**Inspect**

- `.env`
- `frontend/src/config.js`
- `frontend/src/services/http.js`
- `backend/app/config.py`

**Commands**

```bash
docker compose ps backend frontend
curl http://localhost:5001/api/health
docker compose logs --tail=100 frontend backend
```

**Suggested fix**

Use a browser-reachable URL such as `http://localhost:5001/api`, restart the
frontend after changing Vite variables, and include the frontend origin in
`CORS_ORIGINS`.

## Database Connection Fails

**Symptoms**

- Health endpoint returns `503` and `database: unavailable`.
- Psycopg connection errors.
- Backend cannot resolve or connect to PostgreSQL.

**Likely causes**

- Wrong hostname for the execution context.
- PostgreSQL is unhealthy.
- Credentials/database names do not match.
- Port conflict on the host.

**Inspect**

- `DATABASE_URL`
- `docker-compose.yml`
- PostgreSQL service logs

**Commands**

```bash
docker compose ps postgres
docker compose logs --tail=200 postgres
docker compose exec postgres pg_isready -U seniormate -d seniormate
docker compose exec backend python -c "from app import create_app; print(create_app().config['SQLALCHEMY_DATABASE_URI'])"
```

**Suggested fix**

Use `postgres:5432` from a container and `localhost:5432` from the host. Align
database name, username, and password across Compose and the URL.

## Migrations Fail

**Symptoms**

- `flask db upgrade` reports missing revisions or SQL errors.
- Model and database columns differ.
- A migration cannot apply to existing rows.

**Likely causes**

- Database is on an unexpected revision.
- Branches introduced divergent migration heads.
- Generated migration has an unsafe non-null column.
- Manual schema edits bypassed Alembic.

**Inspect**

- `backend/migrations/versions/`
- `backend/migrations/env.py`
- Changed model

**Commands**

```bash
docker compose exec backend flask --app run:app db current
docker compose exec backend flask --app run:app db heads
docker compose exec backend flask --app run:app db history
docker compose exec backend flask --app run:app db upgrade
```

**Suggested fix**

Identify the real current revision before changing anything. Resolve multiple
heads with a merge migration, and use server defaults or staged nullability
when existing rows need a new required value. Never stamp a production
database merely to silence an error.

## MinIO Upload Fails

**Symptoms**

- API returns `Private file storage is unavailable`.
- Connection refused on `localhost:9000` from the backend container.
- Upload metadata is not created.

**Likely causes**

- Backend uses the host endpoint instead of Compose DNS.
- MinIO is stopped.
- Credentials do not match root credentials.
- Bucket operation is denied.

**Inspect**

- `MINIO_ENDPOINT` and `MINIO_DOCKER_ENDPOINT`
- `backend/app/storage.py`
- `docker-compose.yml`

**Commands**

```bash
docker compose ps minio
docker compose logs --tail=200 minio backend
docker compose exec backend python -c "from app import create_app; print(create_app().config['MINIO_ENDPOINT'])"
curl http://localhost:9000/minio/health/live
```

**Suggested fix**

Use `http://minio:9000` inside the backend container. Align access keys,
restart the services, and verify MinIO health before retrying.

## Keycloak Login Fails

**Symptoms**

- Redirect loop.
- Keycloak page says client or redirect URI is invalid.
- Frontend shows authentication unavailable.

**Likely causes**

- Keycloak is not running.
- Wrong realm/client URL.
- Redirect URI or web origin missing in realm import.
- Host/port mismatch.

**Inspect**

- `frontend/src/auth.js`
- `frontend/src/config.js`
- `keycloak/seniormate-realm.json`
- `.env`

**Commands**

```bash
docker compose ps keycloak
docker compose logs --tail=200 keycloak frontend
curl http://localhost:8080/realms/seniormate/.well-known/openid-configuration
```

**Suggested fix**

Confirm realm `seniormate`, client `seniormate-frontend`, frontend URL, and
allowed redirect URIs agree. Restart Keycloak after changing the imported
development realm or update the active realm through its admin console.

## JWT Validation Fails

**Symptoms**

- Login succeeds but API returns `401 Invalid or expired access token`.
- Backend cannot fetch JWKS.
- Token audience or issuer errors appear in tests/logs.

**Likely causes**

- `KEYCLOAK_ISSUER` does not exactly match the token `iss`.
- `KEYCLOAK_AUDIENCE` is absent from the token.
- Backend JWKS URL uses an unreachable hostname.
- Token expired or system time is wrong.

**Inspect**

- `backend/app/auth.py`
- Backend Keycloak environment values
- Keycloak client/audience configuration

**Commands**

```bash
docker compose logs --tail=200 backend keycloak
docker compose exec backend python -c "from app import create_app; a=create_app(); print(a.config['KEYCLOAK_ISSUER'], a.config['KEYCLOAK_JWKS_URL'], a.config['KEYCLOAK_AUDIENCE'])"
curl http://localhost:8080/realms/seniormate/protocol/openid-connect/certs
```

**Suggested fix**

Keep the issuer browser-visible if that is what Keycloak signs, use
`http://keycloak:8080/.../certs` for container-to-container JWKS access, and
ensure the access token includes `seniormate-api` as audience.

## Role Permissions Do Not Work

**Symptoms**

- Button visibility and API behavior disagree.
- Admin screen returns `403`.
- Newly added endpoint is always forbidden.

**Likely causes**

- Frontend and backend permission maps differ.
- Token role is not an approved SeniorMate role.
- New route path is missing from backend resource mapping.
- User needs a fresh token after role changes.

**Inspect**

- `backend/app/auth.py`
- `frontend/src/permission-policy.js`
- `frontend/src/permissions.js`
- `frontend/src/router.js`

**Commands**

```bash
cd backend && .venv/bin/pytest -q tests/test_auth.py tests/test_admin_users.py
cd ../frontend && npm run test:permissions
```

**Suggested fix**

Update both permission maps and tests. Add the route family to
`_resource_for_path()`. Log out and back in after changing Keycloak roles.

## GitHub Actions Fails

**Symptoms**

- PR check is red.
- Local tests pass but CI install/build fails.
- Pages deployment cannot find a Pages site.

**Likely causes**

- Lockfile and package metadata differ.
- Dependency/tool version differs from local.
- Workflow path or permissions are wrong.
- Pages is not configured to use GitHub Actions.

**Inspect**

- `.github/workflows/`
- Failing job and step logs
- Relevant lockfiles

**Commands**

```bash
cd backend && .venv/bin/ruff check . && .venv/bin/pytest
cd ../frontend && npm ci && npm run build
cd ../docs-site && npm ci && npm run build
docker compose config
```

**Suggested fix**

Reproduce the exact CI command locally. Commit lockfile updates. For Pages,
select GitHub Actions under repository Settings -> Pages and rerun the
workflow. Keep workflow permissions limited to what the deployment requires.

## Docker Compose Networking Issues

**Symptoms**

- One container cannot resolve another.
- `localhost` connection refused inside a container.
- Host can reach a service but backend cannot.

**Likely causes**

- Hostname belongs to the wrong network context.
- Service is not on the Compose network.
- Port mapping is confused with container port.

**Inspect**

- `docker-compose.yml`
- Effective environment from `docker compose config`

**Commands**

```bash
docker compose ps
docker compose exec backend getent hosts postgres minio keycloak
docker compose exec backend curl -I http://keycloak:8080
```

**Suggested fix**

Use service names and container ports between containers. Use localhost and
published ports only from the host.

## CORS Issues

**Symptoms**

- Browser console reports a CORS policy error.
- Curl succeeds but browser request fails.
- OPTIONS/preflight fails.

**Likely causes**

- Frontend origin absent from `CORS_ORIGINS`.
- Scheme, hostname, or port differs.
- Request is being sent to the wrong backend.

**Inspect**

- `backend/app/__init__.py`
- `backend/app/config.py`
- `.env`

**Commands**

```bash
curl -i -X OPTIONS http://localhost:5001/api/patients \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET"
```

**Suggested fix**

Add the exact browser origin, including scheme and port, to `CORS_ORIGINS`.
Restart the backend after environment changes.

## Environment Variable Mistakes

**Symptoms**

- A service uses an unexpected default.
- Boolean flags behave opposite to expectation.
- Changes appear to have no effect.

**Likely causes**

- Variable is absent or misspelled.
- `.env` was changed after containers started.
- Vite variable was not prefixed with `VITE_`.
- Host and container values were mixed.

**Inspect**

- `.env.example`
- Local `.env`
- `docker-compose.yml`
- `backend/app/config.py`
- `frontend/src/config.js`

**Commands**

```bash
docker compose config
docker compose exec backend env | sort
docker compose exec frontend env | sort
```

**Suggested fix**

Compare against `.env.example`, recreate affected containers, and remember that
frontend environment values are read by Vite and exposed to the browser.
