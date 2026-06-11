# Backup and Restore

SeniorMate state spans PostgreSQL, MinIO, and Keycloak. A complete recovery
plan must protect all three systems and the environment configuration used to
connect them.

## PostgreSQL

Example logical backup:

```bash
docker compose exec -T postgres \
  pg_dump -U seniormate -d seniormate --format=custom > seniormate.dump
```

Example restore into an empty database:

```bash
docker compose exec -T postgres \
  pg_restore -U seniormate -d seniormate --clean --if-exists < seniormate.dump
```

Use environment-specific users and database names outside local development.

## MinIO

Back up the configured private bucket with an approved S3-compatible backup
tool or storage snapshot. Preserve object keys exactly because PostgreSQL
metadata references them.

## Keycloak

Back up the Keycloak database or use the deployment's supported realm export
process. The checked-in realm JSON is a development bootstrap, not a backup of
live users, credentials, or later configuration changes.

## Configuration

Back up deployment manifests and secret references, but never place secret
values in the repository. Record image versions and migration revision.

## Restore Order

1. Restore PostgreSQL and apply the expected migration revision.
2. Restore MinIO objects and bucket access policy.
3. Restore Keycloak users, clients, roles, and keys.
4. Restore application configuration and start services.
5. Verify health, login, representative downloads, and role enforcement.

Test recovery regularly in an isolated environment. Commands above are
examples and must be adapted to the production platform.
