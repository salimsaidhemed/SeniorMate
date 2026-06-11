# Common Administrative Tasks

## Check Service Health

Open `http://localhost:5001/api/health` locally or the deployment equivalent.
Confirm the API and database are available.

## Add or Disable a User

Use **Admin > Users**. Prefer disabling when access must stop immediately but
identity history should remain.

## Change a Role

Update the user's roles, then ask the user to sign out and sign back in.

## Update Branding

Use **Settings > Branding**, review the live preview, and save. Verify the
navigation shell and login transition afterward.

## Refresh Demo Data

Confirm the environment is non-production and demo mode is enabled, then run
`flask seed-demo`. Use `flask clear-demo` to remove only demo-marked records.

## Apply Database Migrations

```bash
docker compose exec backend flask db upgrade
```

Back up data before production migrations and review the target revision.

## Investigate Upload Failures

Confirm MinIO is running, credentials match, the bucket is reachable, and the
file type and size satisfy the configured policy.

## Investigate Login Failures

Confirm Keycloak is reachable, issuer and audience match, and frontend/backend
auth flags are aligned.
