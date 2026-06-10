# Local Keycloak Setup

SeniorMate includes a development-only Keycloak realm import for testing login,
logout, token refresh, and role-based permissions. Authentication remains
disabled unless both the backend and frontend feature flags are enabled.

## Start the Authenticated Stack

Create `.env` from the example and set:

```bash
AUTH_ENABLED=true
VITE_AUTH_ENABLED=true
```

Start the Compose profile:

```bash
docker compose --profile auth up --build
```

Open:

- SeniorMate: `http://localhost:5173`
- Keycloak: `http://localhost:8080`
- Keycloak admin console: `http://localhost:8080/admin`
- Swagger UI: `http://localhost:5001/api/docs`

The local admin username is `admin` and its placeholder password is
`change-me-local-only`. These credentials are for local development only.

## Imported Realm

The file `keycloak/seniormate-realm.json` creates:

- Realm: `seniormate`
- Public PKCE client: `seniormate-frontend`
- Bearer-only API audience: `seniormate-api`
- Confidential admin service client: `seniormate-admin-api`
- Roles: `admin`, `manager`, `nurse`, `caregiver`, `viewer`
- Groups under `/seniormate-admins` and `/orgs/default/*`

The frontend client adds `seniormate-api` to access-token audiences and includes
group membership in tokens. It has no client secret.

The backend service client uses the client-credentials flow and receives only
the realm-management roles needed to view and manage users. Configure it with:

```bash
KEYCLOAK_BASE_URL=http://keycloak:8080
KEYCLOAK_REALM=seniormate
KEYCLOAK_ADMIN_CLIENT_ID=seniormate-admin-api
KEYCLOAK_ADMIN_CLIENT_SECRET=change-me-local-only
```

The checked-in value is a local placeholder. Use a secret manager and rotate
the client secret outside local development.

## Development Users

Each local user uses the placeholder password `change-me-local-only`:

| Username | Role |
| --- | --- |
| `admin.demo` | admin |
| `manager.demo` | manager |
| `nurse.demo` | nurse |
| `caregiver.demo` | caregiver |
| `viewer.demo` | viewer |

Delete or replace these users in any non-local environment.

## Authorization Behavior

- `/api/health`, Swagger UI, and the OpenAPI JSON remain public.
- Other `/api/*` routes require a bearer token when `AUTH_ENABLED=true`.
- The backend validates signature, issuer, audience, and expiry using the
  Keycloak realm JWKS.
- Frontend route guards improve navigation UX; backend permission checks remain
  authoritative.
- With `AUTH_ENABLED=false`, the backend uses a local development identity and
  existing tests do not contact Keycloak.
- Admin users can manage realm users at `http://localhost:5173/admin/users`.
  Other SeniorMate roles cannot access the navigation item or backend routes.

## Swagger Authorization

1. Sign in to SeniorMate.
2. In browser developer tools, inspect a request to `/api/*`.
3. Copy its `Authorization` request header value.
4. Open Swagger UI and select **Authorize**.
5. Paste the complete `Bearer <token>` value.

Tokens are short-lived. Repeat these steps after expiry if Swagger returns
`401`.

## Reset the Realm

Keycloak imports the realm when its data volume is empty. To recreate the local
realm from the checked-in import:

```bash
docker compose --profile auth down
docker volume rm seniormate_keycloak_data
docker compose --profile auth up --build
```

Removing the Keycloak volume deletes local users and realm changes.
