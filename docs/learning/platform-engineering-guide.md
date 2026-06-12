# Platform Engineering Guide

SeniorMate is an application repository, but its local platform is a compact
example of platform engineering concerns: service orchestration,
configuration, identity, persistence, delivery automation, and operational
boundaries.

## Docker Compose as the Local Platform

`docker-compose.yml` declares the local service graph:

- PostgreSQL
- MinIO
- Keycloak
- Flask backend
- Vue/Vite frontend

Compose gives developers one repeatable command:

```bash
docker compose up --build
```

It also describes health dependencies, ports, persistent volumes, source-code
mounts, and environment injection. This is a developer platform contract.

## Environment Variables

`.env.example` is the configuration catalog and safe starting point. Values
flow into Compose, then into application containers.

Principles:

- Commit placeholders, never real secrets.
- Keep frontend variables prefixed with `VITE_`; they are compiled into the
  browser bundle and must not contain secrets.
- Treat backend secrets as runtime values.
- Document units for numeric values such as byte limits.
- Keep host and container endpoints distinct.

Use `docker compose config` to see the fully resolved Compose configuration.

## Service Discovery

Compose creates a private network and DNS names matching service names.

Inside the backend container:

- PostgreSQL is `postgres:5432`.
- MinIO is `minio:9000`.
- Keycloak is `keycloak:8080`.

From the host browser:

- Flask is `localhost:5001`.
- MinIO API is `localhost:9000`.
- Keycloak is `localhost:8080`.

The backend uses a browser-visible Keycloak issuer but a container-visible
JWKS/Admin endpoint. This split is intentional: token `iss` must match what
Keycloak publishes, while server-to-server calls use Compose DNS.

## PostgreSQL Persistence

The `postgres_data` named volume preserves database files across container
recreation.

Operational lessons:

- `docker compose down` preserves named volumes.
- `docker compose down -v` deletes local persisted data.
- Schema state is managed with Alembic migrations, not container startup SQL.
- Back up PostgreSQL separately from MinIO.

Useful checks:

```bash
docker compose exec postgres pg_isready -U seniormate -d seniormate
docker compose exec postgres psql -U seniormate -d seniormate
docker compose exec backend flask --app run:app db current
```

## MinIO Object Storage

MinIO provides an S3-compatible private bucket. PostgreSQL stores metadata and
object keys; MinIO stores bytes.

This separation teaches:

- Object lifecycle management.
- Metadata versus blob storage.
- Private download mediation.
- Compensating cleanup when one half of a cross-system operation fails.

The current adapter automatically creates the bucket on first upload. A
production platform should provision buckets and policies explicitly.

## Keycloak Identity Provider

Keycloak owns:

- Users and credentials.
- Login and sessions.
- Realm/client roles.
- Signed tokens and JWKS.

SeniorMate owns:

- Permission mapping.
- API enforcement.
- UI visibility.
- Domain records and business operations.

The local realm import makes development repeatable. A production platform
would manage realm configuration as versioned infrastructure, protect admin
client secrets, use TLS, and define backup/restore procedures.

## GitHub Actions CI/CD

Current workflows validate:

- Backend dependencies, Ruff, and Pytest.
- Frontend dependency installation and build.
- Docker Compose configuration and application images.
- VitePress website build and GitHub Pages deployment.

The application delivery process stops at validation. Images are not pushed
to a registry and the runtime application is not deployed automatically.

This is a useful maturity boundary:

```text
Current: source -> test -> build
Future:  source -> test -> scan -> package -> attest -> deploy -> verify
```

## GitHub Pages

The public site lives in `docs-site/`. Its VitePress base is `/SeniorMate/`
because it is a project page, not a user root page.

The workflow:

1. Checks out `main`.
2. Configures Node and Pages.
3. Runs `npm ci`.
4. Builds VitePress.
5. Uploads `.vitepress/dist`.
6. Deploys to the `github-pages` environment.

Repository Pages settings must use GitHub Actions as the source.

## Release and Versioning

SeniorMate uses Semantic Versioning. Version `1.0.0` appears in:

- Frontend package metadata.
- Backend version metadata.
- Health/OpenAPI responses.
- Application footer.
- Changelog and release notes.

A release process should keep code version, documentation, tag, and GitHub
Release aligned.

## Observability Gaps

The current platform has application/container logs and health checks, but no
full observability stack.

Future improvements:

- Structured JSON logging with request and correlation IDs.
- Metrics for request latency, error rates, database pool, uploads, and auth.
- Distributed tracing across frontend/API/external services where practical.
- PostgreSQL, MinIO, and Keycloak health dashboards.
- Alerting and service-level objectives.
- Audit logging for clinical and administrative actions.
- Central log retention and redaction rules.

## Production-Readiness Checklist

### Configuration and secrets

- Replace every development placeholder.
- Store secrets in a managed secret system.
- Validate required configuration at startup.
- Separate development, staging, and production configuration.

### Networking and TLS

- Use HTTPS for frontend, API, Keycloak, and MinIO.
- Restrict PostgreSQL and MinIO from public access.
- Configure trusted proxies and hostnames.
- Set strict CORS origins.

### Data

- Automate PostgreSQL and MinIO backups.
- Test restore procedures.
- Run migrations as a controlled deployment step.
- Define retention and deletion policies.

### Identity and security

- Harden Keycloak and rotate admin-client credentials.
- Review role mappings and token lifetimes.
- Add security headers and dependency/container scanning.
- Add audit logging.
- Perform threat modeling for clinical data.

### Runtime

- Use a production WSGI server and immutable images.
- Add liveness/readiness probes.
- Set resource requests and limits.
- Use restart and rollout policies.
- Remove development source mounts and debug mode.

### Delivery

- Publish versioned images.
- Generate SBOMs and provenance.
- Add staging deployment and smoke tests.
- Require approvals for production.
- Define rollback procedures.

### Observability

- Centralize logs.
- Add metrics, dashboards, alerts, and SLOs.
- Protect sensitive data in telemetry.
