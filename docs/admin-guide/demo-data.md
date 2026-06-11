# Demo Data Administration

Demo data is intended only for local demonstrations and evaluation.

## Safety Rules

- `DEMO_DATA_ENABLED=true` must be set explicitly.
- Commands refuse to run in production mode.
- Demo data never seeds automatically.
- Generated records are marked `is_demo_data=true`.
- Clear operations preserve non-demo records.
- Keycloak demo users are managed separately from clinical seed data.

## Commands

```bash
docker compose exec backend flask db upgrade
docker compose exec backend flask seed-demo
docker compose exec backend flask clear-demo
```

The seed is repeatable: existing demo records are cleared before a fresh
deterministic dataset is created.

See [Demo Data Setup](../setup/demo-data.md) for generated counts,
troubleshooting, and local user accounts.
