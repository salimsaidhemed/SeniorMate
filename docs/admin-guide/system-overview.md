# Administrator System Overview

SeniorMate combines five services:

- Vue/Vuetify web application
- Flask API
- PostgreSQL database
- MinIO private object storage
- Keycloak identity provider

Administrators manage users, roles, organization branding, local demo data,
service health, backups, and environment configuration. Clinical records remain
inside SeniorMate; user credentials remain inside Keycloak.

## Administrative Surfaces

- **Admin > Users**: Keycloak users, enabled status, temporary passwords, and
  SeniorMate roles.
- **Settings > Branding**: app name, organization name, logo, theme colors,
  login banner, and footer.
- **Swagger UI**: developer-oriented API inspection at `/api/docs`.
- **Keycloak Admin Console**: identity-provider administration.
- **MinIO Console**: private object-storage inspection.

## Routine Checks

- Confirm the health endpoint returns success.
- Review failed CI checks before accepting changes.
- Monitor PostgreSQL, MinIO, and Keycloak storage capacity.
- Verify backups through scheduled restore tests.
- Remove development users and placeholder secrets outside local environments.

See [Backup and Restore](backup-restore.md) and the
[Deployment Guide](../technical/deployment-guide.md).
