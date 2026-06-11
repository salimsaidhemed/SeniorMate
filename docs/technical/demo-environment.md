# Demo Environment

The local demo environment combines the imported Keycloak realm with guarded
fictional clinical data.

## Start

```bash
cp .env.example .env
docker compose up --build
docker compose exec backend flask db upgrade
```

Set `DEMO_DATA_ENABLED=true`, recreate the backend, then seed:

```bash
docker compose up -d --force-recreate backend
docker compose exec backend flask seed-demo
```

## Demo Users

The realm includes `admin.demo`, `manager.demo`, `nurse.demo`,
`caregiver.demo`, and `viewer.demo`. Each uses the local placeholder password
documented in [Local Keycloak Setup](../setup/keycloak-local-setup.md).

## Reset

```bash
docker compose exec backend flask clear-demo
```

This removes demo-marked domain data only. For a total local reset, stop the
stack and remove volumes; that also removes local identity and object-storage
state.

Never expose this configuration on a public network or reuse demo credentials
in another environment.
