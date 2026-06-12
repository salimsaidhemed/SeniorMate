# Platform Engineering Guide

SeniorMate is an application repository, but its local platform is a compact
example of platform engineering concerns: service orchestration,
configuration, identity, persistence, delivery automation, and operational
boundaries.

## What Is Platform Engineering?

Platform engineering creates reusable paths, tools, and infrastructure that
help developers build and operate software consistently. SeniorMate's current
platform is small, but its Compose stack, environment contract, identity
provider, object store, database, and CI workflows form an internal developer
platform for this application.

The goal is not merely to run containers. It is to make the safe path the
repeatable path.

## What Is Docker?

Docker packages an application and its runtime dependencies into images and
runs them as isolated containers. Images are immutable build artifacts;
containers are running instances.

SeniorMate uses Docker to make Python, Node, PostgreSQL, MinIO, and Keycloak
versions repeatable across development machines.

Docker concepts in SeniorMate:

| Docker topic | SeniorMate example |
| --- | --- |
| Image | `python:3.12-slim`, `node:20-alpine`, PostgreSQL, MinIO, Keycloak |
| Container | Running `seniormate-backend` or `seniormate-postgres` |
| Volume | `postgres_data`, `minio_data`, `keycloak_data` |
| Network | Compose default network and service-name DNS |
| Port mapping | Host `5001` to backend container `5000` |
| Bind mount | `./backend:/app` for development source |
| Compose | `docker-compose.yml` local platform definition |

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

### Understanding the Docker Design

Compose is appropriate for a single-machine development platform with five
services and named persistence. Kubernetes would add scheduling, rollout,
service, secret, and health-management capabilities, but it would add
substantial local and operational complexity before SeniorMate has a
production cluster requirement.

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

### What Is Object Storage?

Object storage keeps binary data as named objects in buckets rather than rows
or mounted filesystem paths. Each object has a key, bytes, and metadata.

MinIO provides an S3-compatible private bucket. PostgreSQL stores metadata and
object keys; MinIO stores bytes.

This separation teaches:

- Object lifecycle management.
- Metadata versus blob storage.
- Private download mediation.
- Compensating cleanup when one half of a cross-system operation fails.

The current adapter automatically creates the bucket on first upload. A
production platform should provision buckets and policies explicitly.

SeniorMate mapping:

| SeniorMate concept | Object-storage concept |
| --- | --- |
| Medical Records | Private objects plus PostgreSQL metadata |
| Patient Photos | Objects under patient profile keys |
| Branding Logos | Private branding objects |
| `MINIO_BUCKET` | Bucket |
| `storage_object_key` | Object key |
| Download endpoint | Backend-mediated private object read |

Presigned URLs are time-limited signed links that allow direct object access
without making a bucket public. SeniorMate currently streams downloads through
Flask; presigned URLs are a possible future optimization.

### Why MinIO instead of Azure Blob Storage?

MinIO provides S3-compatible object storage that runs locally in Docker
Compose and avoids requiring a cloud account for development. Azure Blob
Storage would provide a managed Azure service with platform-native identity,
durability, and operations, but would make local/offline parity and
cloud-neutral development more complicated.

Tradeoff: SeniorMate gains portable local storage, while production operators
must own MinIO provisioning, durability, upgrades, and monitoring unless they
replace the adapter with a managed S3-compatible service.

### MinIO Learning Resources

**Beginner**

- [MinIO Linux Documentation](https://min.io/docs/minio/linux/index.html)
- [S3 API Concepts](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)

**Intermediate**

- [MinIO Object Management](https://min.io/docs/minio/linux/administration/object-management.html)
- [MinIO Python SDK](https://min.io/docs/minio/linux/developers/python/minio-py.html)

**Official**

- [MinIO Documentation](https://min.io/docs/)

**Suggested experiments**

1. Upload a medical record and locate its object in the MinIO console.
2. Compare the PostgreSQL metadata row with the MinIO object key.
3. Delete an object manually in a disposable environment and observe the
   download endpoint's missing-object behavior.
4. Build a short-lived presigned URL in an isolated experiment without
   replacing the current private download route.

## Keycloak Identity Provider

### What Is Keycloak?

Keycloak is an open-source identity and access management server. It implements
standards including OAuth 2.0 and OpenID Connect (OIDC), manages users and
sessions, issues signed tokens, and provides role/group administration.

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

Key concepts:

- **OAuth 2.0:** Authorization framework for delegated access.
- **OIDC:** Identity layer on OAuth 2.0 that defines login and identity claims.
- **JWT:** Signed token format used for SeniorMate access tokens.
- **Realm:** Isolated Keycloak security domain; SeniorMate uses `seniormate`.
- **Client:** Application registered with Keycloak.
- **Roles:** Claims mapped to SeniorMate permissions.
- **Groups:** Hierarchical user organization available for future org mapping.

SeniorMate mapping:

| SeniorMate concept | Identity concept |
| --- | --- |
| Login redirect | OIDC Authorization Code flow with PKCE |
| `seniormate-frontend` | Public OIDC client |
| `seniormate-api` | API audience/client |
| admin/manager/nurse/caregiver/viewer | Realm/client roles and RBAC inputs |
| Admin -> Users | Keycloak Admin API |
| JWKS validation | JWT signature verification |

### Why Keycloak instead of Auth0?

Keycloak is self-hostable, open source, locally runnable, and gives SeniorMate
control over realm configuration and identity data. Auth0 offers a managed
identity platform with less operational burden, polished hosted experiences,
and vendor support, but introduces external tenancy, pricing, and provider
dependency.

Tradeoff: Keycloak reduces vendor lock-in and improves local parity, while the
SeniorMate operator becomes responsible for upgrades, availability, backup,
TLS, and security hardening.

### Keycloak Learning Resources

**Beginner**

- [Keycloak Getting Started Guides](https://www.keycloak.org/guides#getting-started)
- [OpenID Connect Introduction](https://openid.net/connect/)

**Intermediate**

- [Keycloak Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/)
- [Keycloak Securing Applications Guide](https://www.keycloak.org/docs/latest/securing_apps/)
- [OAuth 2.0 Overview](https://oauth.net/2/)
- [JWT Introduction](https://jwt.io/introduction)

**Official**

- [Keycloak Documentation](https://www.keycloak.org/documentation)

**Suggested experiments**

1. Decode a development access token and locate issuer, audience, expiry, and
   roles without sharing the token.
2. Change a demo user's role, log in again, and compare UI/API access.
3. Temporarily shorten token lifetime in a disposable realm and observe
   refresh behavior.
4. Add a learning-only realm group and inspect the resulting token claims.

## GitHub Actions CI/CD

### What Is GitHub Actions?

GitHub Actions is a workflow automation service integrated with GitHub.
Workflow YAML files react to events and run jobs on hosted or self-hosted
runners.

Core concepts:

- **Workflow:** One YAML automation definition.
- **Event:** Pull request, push, manual dispatch, or another trigger.
- **Job:** Group of steps executed on one runner.
- **Runner:** Machine that performs a job.
- **Action:** Reusable packaged workflow step.
- **Artifact:** File bundle passed between jobs or retained after a run.
- **Environment/deployment:** Protected deployment target and recorded release.

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

SeniorMate mapping:

| SeniorMate concept | GitHub Actions concept |
| --- | --- |
| Backend CI | Workflow with lint/test job |
| Frontend CI | Workflow with npm build job |
| Docker validation | Workflow using runner Docker |
| GitHub Pages | Build artifact plus deployment job/environment |
| PR checks | Pull-request workflow events |

### GitHub Actions Learning Resources

**Beginner**

- [Understanding GitHub Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions)
- [Quickstart for GitHub Actions](https://docs.github.com/en/actions/writing-workflows/quickstart)

**Intermediate**

- [Workflow Syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
- [Store and Share Data with Artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)
- [Deployments and Environments](https://docs.github.com/en/actions/deployment)
- [Security Hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

**Official**

- [GitHub Actions Documentation](https://docs.github.com/actions)

**Suggested experiments**

1. Add a manual `workflow_dispatch` input to a throwaway branch workflow.
2. Upload a small generated test report as an artifact.
3. Add a job dependency and observe execution order.
4. Compare a failed step, failed job, and skipped dependent job.

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

GitHub Pages is a deployment example: the build job creates a static artifact,
and the deploy job publishes it to the `github-pages` environment.

## Release and Versioning

SeniorMate uses Semantic Versioning. Version `1.0.0` appears in:

- Frontend package metadata.
- Backend version metadata.
- Health/OpenAPI responses.
- Application footer.
- Changelog and release notes.

A release process should keep code version, documentation, tag, and GitHub
Release aligned.

## Docker Learning Resources

### Beginner

- [Docker Get Started](https://docs.docker.com/get-started/)
- [Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/)

### Intermediate

- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Compose Networking](https://docs.docker.com/compose/how-tos/networking/)
- [Volumes](https://docs.docker.com/engine/storage/volumes/)
- [Build Best Practices](https://docs.docker.com/build/building/best-practices/)

### Official Documentation

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### Suggested Docker Experiments

1. Run `docker compose config` and trace one resolved variable.
2. Enter the backend container and resolve `postgres`, `minio`, and `keycloak`.
3. Stop/recreate PostgreSQL and prove named-volume persistence.
4. Rebuild the backend after a requirements change and compare image layers.
5. Use `docker compose down` versus `down -v` in a disposable environment.

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
