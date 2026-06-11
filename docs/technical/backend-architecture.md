# Backend Architecture

The backend is a Flask application factory in `backend/app/__init__.py`.

## Main Layers

- **Configuration**: environment-backed settings in `app/config.py`.
- **Extensions**: SQLAlchemy, Flask-Migrate, CORS, and Swagger initialization.
- **Models**: SQLAlchemy domain entities in `app/models/`.
- **Routes**: resource blueprints in `app/routes/`.
- **Authentication**: JWT validation, identity normalization, and centralized
  permission enforcement in `app/auth.py`.
- **Storage**: private MinIO operations in `app/storage.py`.
- **Identity administration**: Keycloak Admin API client in
  `app/keycloak_admin.py`.
- **Demo tooling**: guarded Flask CLI commands in `app/demo_data.py`.

## Request Flow

1. Flask receives an `/api/*` request.
2. Public-path rules or JWT validation establish identity.
3. The permission policy authorizes the resource and HTTP method.
4. The route validates input and queries SQLAlchemy models.
5. Storage or Keycloak services are called only when required.
6. The route returns a consistent JSON envelope or a file/CSV response.

Backend permission checks are authoritative even when the frontend hides an
action.
