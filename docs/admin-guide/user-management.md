# User Management

Administrators manage SeniorMate identities through **Admin > Users**. The
application calls Keycloak Admin API through a server-side service account;
browser clients never receive the admin client secret.

![SeniorMate user management](../images/user-management.jpg)

## Available Actions

- List and inspect users
- Create a user
- Update name, username, email, and verification state
- Enable or disable access
- Assign SeniorMate roles
- Set a temporary password
- Delete a user

Only the `admin` role can use these actions. Managers and other roles cannot
open the page or call the API.

## Create a User

1. Open **Admin > Users**.
2. Select the create action.
3. Enter username, email, name, enabled state, and approved roles.
4. Set an initial temporary password.
5. Give the credential to the user through an approved channel.

SeniorMate never displays or stores an existing password.

## Disable Before Delete

Prefer disabling an account when access must stop but identity history should
remain. Delete only when organizational identity-retention policy permits it.

For implementation details and local client setup, see
[Local Keycloak Setup](../setup/keycloak-local-setup.md) and
[Authentication Design](../architecture/auth-design.md).
