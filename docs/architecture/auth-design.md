# Authentication and Authorization Design

## Status

This document defines the intended authentication and authorization architecture for SeniorMate. It is a design reference only. Authentication, login UI, token validation, and permission enforcement are not implemented by this feature.

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

The first implementation should translate roles into named permissions rather than scattering role-name checks throughout routes. Example permissions include `patients.read`, `patients.write`, `nurse_notes.write`, and `branding.manage`.

Legend:

- **Manage**: create, read, update, and delete.
- **Clinical manage**: create, read, and update clinical records; deletion may require an additional policy or audit action.
- **Assigned manage**: act only on patients or visits assigned to the user.
- **Read**: view only.
- **None**: no access.

| Area | Admin | Manager | Nurse | Caregiver | Viewer |
| --- | --- | --- | --- | --- | --- |
| Dashboard | Read all organization data | Read all organization data | Read permitted clinical data | Read assigned activity | Read permitted summaries |
| Patients | Manage | Manage | Read and update clinical context | Read assigned patients | Read |
| Visits | Manage | Manage | Manage nursing visits | Assigned manage | Read |
| Aide notes | Manage | Manage | Read | Assigned manage | Read |
| Nurse notes | Manage | Read | Clinical manage | None | Read |
| Assessments | Manage | Read | Clinical manage | Create/read assigned basic assessments | Read |
| Medical records | Manage | Manage | Clinical manage | Read assigned records when permitted | Read |
| Patient photos | Manage and verify | Manage and verify | Upload and verify | Upload assigned patients | Read |
| Printable reports | Generate all | Generate all | Generate permitted clinical reports | Generate assigned care reports | Generate read-only reports |
| Branding/settings | Manage | Read | None | None | None |

This matrix is the initial policy proposal. Before implementation, the maintainer should confirm whether viewers may access clinical narrative fields and whether clinical record deletion should be restricted to administrators.

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

Future frontend authentication should:

- Redirect unauthenticated users to Keycloak.
- Restore the intended route after successful login.
- Keep access tokens in memory where practical.
- Refresh sessions through the OIDC client without storing long-lived secrets.
- Use route metadata and permission helpers to hide unavailable actions.
- Treat backend `401` and `403` responses as authoritative.

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

1. Add Keycloak local configuration and OIDC client settings.
2. Add backend JWT validation and normalized identity context.
3. Add permission mapping and protected API decorators/services.
4. Add frontend login, logout, session restoration, and route guards.
5. Add organization scoping to domain records.
6. Add audit logging for sensitive actions.

