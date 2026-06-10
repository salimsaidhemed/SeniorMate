# Roles and Permissions

SeniorMate adapts its navigation, routes, and actions to the roles included in
the signed-in user's Keycloak access token. Backend authorization remains the
security boundary; frontend controls only prevent confusing or predictably
forbidden actions.

## Role Summary

| Role | Typical access |
| --- | --- |
| `admin` | Full application access, branding settings, and user management. |
| `manager` | Manages operational and clinical records plus branding settings. |
| `nurse` | Manages visits, nurse notes, assessments, and medical records. |
| `caregiver` | Reads core records and manages aide notes. |
| `viewer` | Read-only access to records and printable reports. |

## Application Access

| Area | Admin | Manager | Nurse | Caregiver | Viewer |
| --- | --- | --- | --- | --- | --- |
| Dashboard | View | View | View | Hidden | View |
| Patients | Manage | Manage | View | View | View |
| Visits | Manage | Manage | Manage | View | View |
| Aide notes | Manage | Manage | View | Manage | View |
| Nurse notes | Manage | Manage | Manage | View | View |
| Assessments | Manage | Manage | Manage | View | View |
| Medical records | Manage | Manage | Manage | View/download | View/download |
| Patient photos | Manage/verify | Manage/verify | View | View | View |
| Printable reports | View/print | View/print | View/print | View/print | View/print |
| Branding settings | Manage | Manage | Hidden | Hidden | Hidden |
| Admin users | Manage | Hidden | Hidden | Hidden | Hidden |

“Manage” includes the create, edit, and delete actions currently supported by
that screen.

## Restricted Routes

SeniorMate hides navigation links and action buttons when the current user
lacks the required permission. Directly opening a restricted URL displays an
Access Denied page with a link back to an available workspace page.

The API independently validates the access token and permission for every
protected request. A hidden button or frontend route guard is not a security
control.

## Local Development

When `VITE_AUTH_ENABLED=false`, the frontend uses admin-like access so all
workflows remain available without a Keycloak login. Set frontend and backend
auth flags to `true` together when manually testing real roles.
