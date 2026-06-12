# SeniorMate Eight-Week Study Plan

This plan is designed for a developer with limited Flask and Vue experience.
Aim for four to six focused hours each week. Keep a learning journal with:

- New terms.
- Commands used.
- Request paths traced.
- Questions and failures.
- One small artifact or code experiment.

Use fictional/local data only and keep experiments on feature branches.

## Week 1: Docker and Flask Basics

**Study**

- Containers, images, volumes, networks, and Compose.
- Flask routes, requests, responses, contexts, and blueprints.
- SeniorMate's app factory and local service graph.

**Read**

- [Docker Get Started](https://docs.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
- [Flask Backend Guide](flask-backend-guide.md)

**Hands-on**

1. Start the stack and inspect all five services.
2. Trace `/api/health` from Compose port to Flask route.
3. Add and test a temporary learning endpoint, then remove it.

**Outcome**

Explain the difference between image/container and host/container addressing.

## Week 2: SQLAlchemy and PostgreSQL

**Study**

- Tables, keys, relationships, indexes, constraints, and transactions.
- SQLAlchemy model/relationship mapping.
- Alembic migration history.

**Read**

- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [SQLAlchemy ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Data Model Walkthrough](data-model-walkthrough.md)

**Hands-on**

1. Inspect the patient and visit tables in `psql`.
2. Trace model relationships and deletion behavior.
3. Generate a disposable migration for a nullable learning field.

**Outcome**

Explain how model code, migration code, and the live database differ.

## Week 3: Vue Basics and Vuetify

**Study**

- Components, props, refs, computed state, Composition API, and lifecycle.
- Vue Router and Vuetify forms/layout.

**Read**

- [Vue Tutorial](https://vuejs.org/tutorial/)
- [Vue Guide](https://vuejs.org/guide/introduction.html)
- [Vuetify Documentation](https://vuetifyjs.com/)
- [Vue Frontend Guide](vue-frontend-guide.md)

**Hands-on**

1. Add a computed display value to a local view.
2. Build a small Vuetify card and form from static data.
3. Trace route metadata and a permission guard.

**Outcome**

Explain how reactive state causes the rendered UI to update.

## Week 4: REST APIs and Swagger

**Study**

- HTTP methods and status codes.
- JSON request/response design.
- Validation, pagination, and multipart requests.
- OpenAPI and Swagger UI.

**Read**

- [MDN HTTP Overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Swagger OpenAPI Guide](https://swagger.io/docs/specification/v3_0/about/)
- [Request Flows](request-flows.md)

**Hands-on**

1. Create a patient in Swagger.
2. Trigger and inspect a validation error.
3. Compare one runtime parser with its `app/swagger.py` schema.

**Outcome**

Trace an HTTP request from browser/service to route, model, and response.

## Week 5: Keycloak, OAuth 2.0, OIDC, and JWT

**Study**

- OAuth 2.0 authorization.
- OIDC identity.
- Authorization Code with PKCE.
- JWT claims, signatures, issuer, audience, and expiry.
- Keycloak realms, clients, roles, and groups.

**Read**

- [Keycloak Getting Started](https://www.keycloak.org/guides#getting-started)
- [OpenID Connect](https://openid.net/connect/)
- [OAuth 2.0](https://oauth.net/2/)
- Platform guide Keycloak section.

**Hands-on**

1. Inspect development realm clients and roles.
2. Decode a local token safely.
3. Compare viewer and manager access after fresh login.

**Outcome**

Explain why frontend route guards are not the security boundary.

## Week 6: Reporting and Architecture Review

**Study**

- Aggregation queries.
- Filters and CSV output.
- Service boundaries and cross-system workflows.
- PostgreSQL metadata plus MinIO object storage.

**Read**

- `backend/app/routes/reports.py`
- [Architecture Overview](../architecture/overview.md)
- [Request Flows](request-flows.md)

**Hands-on**

1. Trace one report filter into SQLAlchemy conditions.
2. Compare JSON and CSV report output.
3. Upload a medical record and map database/object-store state.

**Outcome**

Draw SeniorMate's architecture from memory and explain each boundary.

## Week 7: CI/CD and GitHub Actions

**Study**

- Workflow triggers, jobs, runners, actions, artifacts, and environments.
- Pull-request validation and GitHub Pages deployment.

**Read**

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Understanding GitHub Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions)
- `.github/workflows/`

**Hands-on**

1. Match every CI step to a local command.
2. Inspect a workflow run and its job logs.
3. Add an artifact step on a temporary branch.

**Outcome**

Explain the path from commit to required checks and Pages deployment.

## Week 8: Production Readiness and Platform Engineering

**Study**

- Secrets, TLS, backups, migrations, immutable images, observability, security,
  deployment safety, and rollback.
- Platform engineering as a paved path for developers.

**Read**

- [Platform Engineering Guide](platform-engineering-guide.md)
- [Deployment Guide](../technical/deployment-guide.md)
- [Backup and Restore](../admin-guide/backup-restore.md)

**Hands-on**

1. Perform a gap assessment using the production-readiness checklist.
2. Design a staging pipeline without implementing production credentials.
3. Propose logs, metrics, traces, dashboards, and alerts for one workflow.

**Outcome**

Produce a prioritized production-readiness backlog with risks and owners.

## Continuing After Week 8

Choose one [learning exercise](exercises.md), implement it through a pull
request, and write a short retrospective:

- What changed across layers?
- Which test caught the most useful issue?
- Which boundary should be improved next?
