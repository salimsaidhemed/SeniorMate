# Authentication and Authorization Design

## Status

SeniorMate now implements the first authentication and authorization layer
described here. The Vue application uses the official Keycloak JavaScript
adapter, while the Flask backend validates JWTs against the realm JWKS and
enforces centralized role-to-permission mappings.

## Architecture Overview

SeniorMate will use Keycloak as its OpenID Connect (OIDC) identity provider. The Vue frontend will initiate login through the Authorization Code flow with PKCE. The Flask backend will accept bearer access tokens and enforce application permissions after validating each token.

The security boundary is deliberately split:

### Keycloak Owns

- User identities and credentials.
- Login, logout, password recovery, and session management.
- Identity federation and future multi-factor authentication.
- Groups and group membership.
- Realm and client roles.
- OIDC identity claims included in tokens.

### SeniorMate Owns

- Mapping trusted Keycloak roles and groups to application permissions.
- Enforcing permissions on every protected backend API.
- Organization settings and branding configuration.
- Patient, visit, clinical note, assessment, document, and reporting data.
- Organization-aware data filtering.
- Audit-friendly business actions and domain event history.

Keycloak answers "who is this user?" SeniorMate answers "what may this user do with this record?"

## Recommended Keycloak Structure

### Realm

- Realm name: `seniormate`

Use one realm for the SeniorMate product initially. Separate environments should use separate Keycloak instances or clearly isolated realm copies rather than sharing production identities with development.

### Clients

| Client | Type | Purpose |
| --- | --- | --- |
| `seniormate-frontend` | Public OIDC client | Vue browser application using Authorization Code with PKCE. |
| `seniormate-api` | API audience/client | Represents the Flask API and expected access-token audience. |
| `seniormate-admin-api` | Confidential service client | Allows the Flask backend to manage realm users through the Keycloak Admin API. |

The frontend client must not contain a client secret. The API should reject tokens that do not include the expected issuer and audience.

### Default Groups

```text
/seniormate-admins
/orgs/default/admins
/orgs/default/managers
/orgs/default/nurses
/orgs/default/caregivers
/orgs/default/viewers
```

- `/seniormate-admins` is reserved for trusted product-level administration.
- `/orgs/default/*` represents the first organization and establishes a structure that can expand to `/orgs/<organization-slug>/*`.
- Group membership should supply organization context and an application role through mapped claims.

### Roles

| Role | Intended responsibility |
| --- | --- |
| `admin` | Organization configuration, user-facing administration, and full clinical/operational access. |
| `manager` | Operational oversight, record management, reporting, and staff coordination. |
| `nurse` | Clinical documentation, assessments, medical records, and assigned patient care. |
| `caregiver` | Visit and aide-note workflows needed to deliver assigned care. |
| `viewer` | Read-only access to permitted organization records and reports. |

Realm roles may identify broad SeniorMate access. Client roles on `seniormate-api` should represent application roles where practical. Group membership remains the preferred source of organization context.

## Permission Model

The implementation translates roles into named permissions in the backend auth
module rather than scattering role-name checks throughout routes. Example
permissions include `patients.read`, `patients.write`, and
`nurse_notes.write`.

| Area | Admin | Manager | Nurse | Caregiver | Viewer |
| --- | --- | --- | --- | --- | --- |
| Dashboard | Read | Read | Read | No access | Read |
| Patients | Manage | Manage | Read | Read | Read |
| Visits | Manage | Manage | Manage | Read | Read |
| Aide notes | Manage | Manage | Read | Manage | Read |
| Nurse notes | Manage | Manage | Manage | Read | Read |
| Assessments | Manage | Manage | Manage | Read | Read |
| Medical records | Manage | Manage | Manage | Read/download | Read/download |
| Patient photos | Manage and verify | Manage and verify | Read | Read | Read |
| Printable reports | Read/print | Read/print | Read/print | Read/print | Read/print |
| Branding/settings | Manage | Manage | Read applied branding | Read applied branding | Read applied branding |
| User management | Manage | No access | No access | No access | No access |

This table reflects the permissions currently enforced by the backend. Future
assignment and organization scoping will narrow record visibility without
making frontend checks authoritative.

## Token and Claim Design

The backend should require and validate:

- Token signature using the realm JSON Web Key Set (JWKS).
- Issuer matching the configured SeniorMate realm.
- Audience containing `seniormate-api`.
- Expiration and not-before timestamps.
- Authorized party/client where appropriate.

Recommended normalized identity context:

```json
{
  "subject": "keycloak-user-id",
  "username": "alex.morgan",
  "organization_id": "default",
  "groups": ["/orgs/default/nurses"],
  "roles": ["nurse"],
  "permissions": ["patients.read", "nurse_notes.write"]
}
```

The exact token shape may use Keycloak's `realm_access`, `resource_access`, and `groups` claims. SeniorMate should normalize those claims once in an authentication layer before route handlers use them.

## Backend Enforcement

- Backend APIs are the authoritative permission boundary.
- Every protected route must validate the JWT before loading or mutating data.
- Permission checks should occur before returning record existence details when possible.
- Domain services should accept an authenticated identity context and enforce organization scope.
- Sensitive actions should record actor, action, target record, timestamp, and outcome when audit logging is introduced.
- Frontend route guards and hidden buttons improve UX only; they are not security controls.

## Frontend Behavior

The frontend authentication layer:

- Redirects unauthenticated users to Keycloak with Authorization Code and PKCE.
- Keeps access tokens in the Keycloak adapter's in-memory state.
- Refreshes short-lived access tokens before API requests and on expiry.
- Adds bearer tokens to JSON, multipart, photo, and document requests.
- Uses a centralized permission policy that mirrors backend permission names.
- Filters navigation using read permissions and hides unavailable actions.
- Uses permission-based route metadata for read, write, report, settings, and
  administration screens.
- Redirects direct navigation to a restricted route to a dedicated Access
  Denied page.
- Treats backend `401` and `403` responses as authoritative.

Authentication is enabled by default in the application and local Compose
stack. `AUTH_ENABLED=false` and `VITE_AUTH_ENABLED=false` provide an explicit
development and test bypass. The frontend assumes the `admin` role in this
mode so existing local workflows remain available. Both flags must use the
same value.

Hidden actions and route guards are usability controls only. They reduce
predictable `403` responses but must never replace backend permission checks.
See [Roles and Permissions](../user-guide/roles-and-permissions.md) for the
user-facing behavior.

Branding settings are readable by authenticated roles. Only `admin` and
`manager` roles receive `branding.write`; the public branding and logo preview
endpoints remain unauthenticated so identity can resolve before login.

## Admin User Management

SeniorMate exposes an admin-only application interface over the Keycloak Admin
API. The backend authenticates with the confidential
`seniormate-admin-api` service account and keeps its client secret server-side.
The browser never calls Keycloak Admin API directly.

- Only the `admin` SeniorMate role receives `user_admin.manage`.
- Managers and other roles receive `403` from all `/api/admin/*` endpoints.
- `AUTH_ENABLED=false` preserves the explicit local development bypass.
- Passwords are write-only: SeniorMate sends new temporary credentials to
  Keycloak and never stores or retrieves them.
- User identities and role mappings remain owned by Keycloak.

## Multi-Organization Direction

Future domain tables should include `organization_id` where records are organization-owned. The backend must derive organization context from validated identity claims and filter every query by that organization. Client-provided organization identifiers must never be trusted as the sole source of scope.

The proposed group hierarchy supports future organizations:

```text
/orgs/acme-home-care/admins
/orgs/acme-home-care/nurses
/orgs/harbor-living/caregivers
```

Cross-organization access should be explicit, rare, and audited.

## Implementation Sequence

1. Completed: Keycloak local configuration and OIDC client settings.
2. Completed: backend JWT validation and normalized identity context.
3. Completed: permission mapping and protected API helpers.
4. Completed: frontend login, logout, token refresh, and route guards.
5. Future: organization scoping for domain records.
6. Future: audit logging for sensitive actions.
