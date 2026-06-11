# Deployment Guide

SeniorMate's current Compose configuration is optimized for local development.
A production deployment must replace development commands and placeholder
security settings.

## Required Services

- Built Vue frontend served by a production web server
- Flask application behind a production WSGI server and reverse proxy
- PostgreSQL with managed persistence and backups
- Private S3-compatible storage or MinIO
- Keycloak with persistent database, TLS, and production configuration

## Environment Configuration

At minimum configure:

- Flask secret, debug disabled, allowed CORS origins
- PostgreSQL URL and credentials
- MinIO endpoint, TLS mode, credentials, bucket, and upload limits
- Keycloak issuer, JWKS URL, audience, realm, and admin service client
- Frontend API and Keycloak public URLs
- Authentication enabled
- Demo data disabled

## Deployment Sequence

1. Provision PostgreSQL, object storage, Keycloak, and secret management.
2. Configure DNS and TLS for frontend, API, Keycloak, and storage.
3. Create/import the Keycloak realm and rotate all local placeholders.
4. Create the private MinIO bucket and least-privileged application access.
5. Build immutable backend and frontend images.
6. Apply database migrations as a controlled release step.
7. Start services and verify health, login, role access, uploads, and reports.
8. Enable monitoring, backups, restore tests, and log retention.

## Keycloak

Use Authorization Code with PKCE for the public frontend client. Configure the
API audience and exact production issuer. Keep the admin client secret only in
the backend secret store.

## PostgreSQL

Do not expose PostgreSQL publicly. Use TLS where supported, scheduled backups,
connection limits, and a dedicated application user.

## MinIO

Keep the bucket private. Use TLS, dedicated credentials, object lifecycle and
backup policies, and no public bucket access.

The repository does not yet claim production hardening, high availability, or
regulatory compliance. Perform a security and compliance review before handling
real protected health information.
