# Local Environment

Copy `.env.example` to `.env`. The example contains local placeholders only.

## Variable Groups

| Group | Key variables |
| --- | --- |
| Flask | `APP_ENV`, `APP_DEBUG`, `APP_SECRET_KEY`, `CORS_ORIGINS` |
| Frontend | `VITE_API_BASE_URL`, `VITE_AUTH_ENABLED`, `VITE_KEYCLOAK_*` |
| PostgreSQL | `DATABASE_URL`, `POSTGRES_*` |
| Authentication | `AUTH_ENABLED`, `KEYCLOAK_ISSUER`, `KEYCLOAK_JWKS_URL`, `KEYCLOAK_AUDIENCE` |
| User admin | `KEYCLOAK_BASE_URL`, `KEYCLOAK_REALM`, `KEYCLOAK_ADMIN_CLIENT_*` |
| MinIO | `MINIO_ENDPOINT`, `MINIO_DOCKER_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_BUCKET` |
| Upload limits | `MEDICAL_RECORD_MAX_FILE_SIZE`, `PATIENT_PHOTO_MAX_FILE_SIZE`, `BRANDING_LOGO_MAX_FILE_SIZE` |
| Demo | `DEMO_DATA_ENABLED` |

## Host and Container Endpoints

The backend container reaches MinIO at `http://minio:9000`; a backend process
running on the host reaches it at `http://localhost:9000`. Keep
`MINIO_DOCKER_ENDPOINT` and `MINIO_ENDPOINT` separate.

The browser-visible Keycloak issuer is `http://localhost:8080/realms/seniormate`,
while the backend container can fetch JWKS through the `keycloak` service.

## Secrets

Replace all placeholder secrets for non-local environments. Use a platform
secret manager rather than committed files or image build arguments.
