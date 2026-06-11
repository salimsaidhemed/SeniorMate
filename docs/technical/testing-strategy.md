# Testing Strategy

SeniorMate uses risk-based automated and manual validation.

## Backend

```bash
cd backend
.venv/bin/ruff check app tests
.venv/bin/pytest -q
```

Pytest covers application creation, health, CRUD, validation, OpenAPI,
authentication, authorization, storage boundaries, admin clients, demo
seeding, reports, and safe empty states. External systems such as Keycloak and
MinIO are mocked where unit tests should remain self-contained.

## Frontend

```bash
cd frontend
npm run test:permissions
npm run build
```

The permission policy has focused Node tests. The production build catches
template, import, and bundling errors. User workflows and responsive layouts
are verified in the local browser until broader component testing is added.

## Docker

```bash
docker compose config
docker compose build backend frontend
```

## Documentation

Check relative Markdown links, Mermaid syntax, secret-like text, and screenshots
before publishing. Screenshots must contain fictional data only.
