# Admin User Management

SeniorMate administrators can manage Keycloak identities from **Admin → Users**
without leaving the application. Keycloak remains the identity provider and
stores all credentials, sessions, and role mappings.

## Available Actions

- List and search realm users.
- Create users with a temporary password.
- Edit names, username, email, enabled status, and email verification state.
- Assign the SeniorMate roles `admin`, `manager`, `nurse`, `caregiver`, and
  `viewer`.
- Enable or disable sign-in.
- Set a new temporary password.
- Delete a Keycloak user.

Only users with the `admin` role can open the page or call its backend APIs.
Managers cannot create users or assign roles. When `AUTH_ENABLED=false`, the
page remains available for explicit local development.

## Password Safety

SeniorMate never displays, retrieves, or stores a user's password. Create and
reset actions send the new value directly from the backend to Keycloak. New
passwords are temporary by default, so the user must replace them after the
next sign-in.

## Keycloak Service Client

The Flask backend uses the confidential `seniormate-admin-api` service account.
It requires Keycloak realm-management permissions for viewing, querying, and
managing users. Its secret belongs in environment configuration and must never
be exposed to the frontend.

See [../setup/keycloak-local-setup.md](../setup/keycloak-local-setup.md) for
local environment values and realm import instructions.
