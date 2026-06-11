# Docker Compose

The root `docker-compose.yml` defines the complete local stack.

| Service | Purpose | Local port |
| --- | --- | --- |
| `frontend` | Vue/Vite development server | 5173 |
| `backend` | Flask API | 5001 |
| `postgres` | Application database | 5432 |
| `minio` | Private object storage and console | 9000, 9001 |
| `keycloak` | OIDC identity provider | 8080 |

## Persistent Volumes

- `postgres_data`
- `minio_data`
- `keycloak_data`
- `frontend_node_modules`

## Common Commands

```bash
docker compose up --build
docker compose ps
docker compose logs -f backend
docker compose exec backend flask db upgrade
docker compose down
```

`docker compose down -v` deletes local database, object-store, Keycloak, and
frontend dependency volumes. Use it only when a complete local reset is
intended.

The backend waits for healthy PostgreSQL and started MinIO and Keycloak
services. The frontend starts after the backend service is available.
