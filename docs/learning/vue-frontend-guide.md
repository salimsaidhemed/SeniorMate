# Vue Frontend Guide

This guide explains how the SeniorMate Vue 3 frontend is assembled and how a
user action becomes an authenticated API request and a UI update.

## Application Bootstrap

[`frontend/src/main.js`](../../frontend/src/main.js) is the entry point.

It:

1. Imports Vuetify, icons, and global CSS.
2. Loads public branding.
3. Initializes Keycloak authentication.
4. Imports the router after auth initialization.
5. Creates the SeniorMate Vuetify theme.
6. Registers shared components globally.
7. Mounts `App`.

Branding loads before rendering so the shell can begin with the configured
name, logo, and colors instead of visibly changing after mount.

## Vue Style Used in SeniorMate

The project uses Vue's Composition API primitives inside JavaScript component
objects:

- `ref()` for mutable values.
- `reactive()` for shared state.
- `computed()` for derived values.
- `onMounted()` for initial loading.
- `useRoute()` and `useRouter()` for navigation.

Components use JavaScript template strings rather than `.vue` single-file
components. A view exports an object with `setup()` and `template`.

## Router

`src/router.js` defines:

- List, detail, create, edit, and print routes.
- Report routes.
- Admin and branding routes.
- An Access Denied route.

Most routes include `meta.permission`. The global `beforeEach` guard:

1. Allows the authentication error screen to render.
2. Starts login if the user is unauthenticated.
3. Checks the required permission.
4. Redirects unauthorized users to `/access-denied`.

The guard improves user experience. It is not a security boundary; Flask must
still reject unauthorized API calls.

## Vuetify Layout

`src/views/App.js` defines the application shell:

- Responsive navigation drawer.
- Permission-filtered navigation.
- Organization branding.
- User name and role.
- Logout action.
- Version display.
- Application bar and route content.

Reusable UI components standardize common patterns:

- `PageHeader`
- `DetailHeader`
- `SectionCard`
- `LoadingState`
- `EmptyState`
- `ErrorAlert`
- `ConfirmDialog`
- `StatusChip`
- Print components

Views should reuse these before inventing another local pattern.

## Views and Components

Views under `src/views/` correspond to router destinations. They own page-level
loading, forms, API calls, and navigation.

Components under `src/components/` encapsulate repeated UI or a substantial
section inside a page. `MedicalRecordsSection`, for example, owns upload,
metadata edit, download, and delete behavior within Patient Detail.

A useful split is:

- View: route ownership and page composition.
- Component: reusable presentation or a focused embedded workflow.
- Service: HTTP request details.

## API Services

`src/services/http.js` is the common HTTP adapter.

`apiRequest()`:

1. Refreshes or retrieves the Keycloak access token.
2. Creates the API URL from `VITE_API_BASE_URL`.
3. Adds JSON content type unless the body is `FormData`.
4. Adds the bearer token.
5. Calls `fetch`.
6. Parses JSON and throws an `Error` with the API payload on failure.

`apiBlobRequest()` performs authenticated downloads.

Domain service files such as `patients.js`, `visits.js`, and
`medicalRecords.js` keep paths and HTTP verbs out of views.

## State Management

SeniorMate does not use Pinia or Vuex.

Shared reactive modules provide the current global state:

- `auth.js`: authentication status, profile, roles, and token availability.
- `branding.js`: resolved public branding and theme values.

Page state stays local to views and components using refs. This is appropriate
while most data is route-specific. A central store becomes valuable if the
same server state needs caching, synchronization, or optimistic updates across
many unrelated views.

## Authentication State

`auth.js` wraps `keycloak-js`.

Authentication-enabled behavior:

- `login-required` on startup.
- Authorization Code with PKCE S256.
- Token refresh before API requests.
- A 30-second refresh timer.
- Login retry when a token expires or refresh fails.
- User profile and roles extracted from token claims.

Authentication-disabled behavior:

- The frontend creates a Development User.
- The user receives the `admin` role.
- Existing screens remain usable without Keycloak.

Frontend and backend auth flags must agree during local development.

## Permission Helpers and RBAC UI

`permission-policy.js` is a pure role-to-permission map. It is deliberately
separate from Vue so Node's built-in test runner can test it.

`permissions.js` connects the pure policy to current `authState.roles` and
provides helpers such as:

- `can(permission)`
- `canManagePatients()`
- `canCreateAideNote()`
- `canManageMedicalRecords()`
- `canManageUsers()`

Navigation and action buttons call these helpers. The frontend map should match
`backend/app/auth.py`. A permission change normally requires updating and
testing both maps.

## Forms and Validation

Forms use Vuetify fields with local validation before submission. For example,
PatientForm checks first and last names, normalizes empty strings, then calls
the patient service.

The backend remains authoritative. On API failure:

- `http.js` throws an error.
- The view displays `error.message`.
- Field errors can be read from `error.payload.errors`.

This two-level approach gives immediate feedback while preserving server-side
integrity.

## User Action-to-UI Walkthrough

Creating a patient:

1. User submits `PatientFormView`.
2. `validate()` checks required names.
3. `apiPayload()` normalizes form data.
4. `createPatient()` calls `apiRequest("/patients", ...)`.
5. `apiRequest()` refreshes the token and sends the bearer request.
6. Flask validates and persists the patient.
7. The service returns the parsed response.
8. The view routes to `/patients/<id>`.
9. Patient Detail loads the patient and related records.

Deleting a patient:

1. Patient List hides the action unless the role can write patients.
2. A confirmation dialog captures intent.
3. The delete service calls the API.
4. On success, the view shows feedback and reloads the list.

## Adding a Frontend Field

For a new patient field:

1. Add it to the backend first.
2. Add it to `emptyForm`.
3. Render the Vuetify field.
4. Include any local validation/normalization.
5. Confirm create and edit preload behavior.
6. Display it in the appropriate detail/print view.
7. Run the production build and browser-check narrow layouts.

## Testing and Verification

Run:

```bash
cd frontend
npm run test:permissions
npm run build
```

The current frontend has limited unit coverage. Also verify:

- Authentication-enabled and disabled startup.
- Role-specific visibility.
- Loading, empty, error, and success states.
- Desktop and narrow browser widths.
- No raw API stack traces are shown.
- No broken image or logo states.
