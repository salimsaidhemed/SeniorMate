# Vue Frontend Guide

This guide explains how the SeniorMate Vue 3 frontend is assembled and how a
user action becomes an authenticated API request and a UI update.

## What Is Vue?

Vue is a progressive JavaScript framework for building reactive user
interfaces. It organizes UI into components and automatically updates rendered
output when reactive state changes.

SeniorMate uses Vue because it supports an approachable component model,
incremental composition, a mature router, and a strong ecosystem without
requiring a large frontend framework.

Vue appears throughout `frontend/src/`:

- `main.js` creates and mounts the application.
- `views/` contains route-level page components.
- `components/` contains reusable UI components.
- `router.js` maps URLs to views.
- `auth.js` and `branding.js` provide reactive shared state.

## What Is Vite?

Vite is the frontend development server and production build tool. It serves
Vue modules quickly during development and bundles optimized static assets for
deployment.

SeniorMate uses Vite through `frontend/package.json`, `frontend/vite.config.js`,
and `VITE_*` environment variables. The local frontend container runs the Vite
development server, while CI runs the production build.

Compared with the older Vue CLI/Webpack approach, Vite offers faster startup
and a simpler modern configuration. The tradeoff is that environment variables
and browser-compatible code must follow Vite conventions.

Resources and experiments:

- [Vite Guide](https://vite.dev/guide/)
- [Vite Environment Variables](https://vite.dev/guide/env-and-mode)
- Change a non-secret `VITE_*` value locally and inspect it through
  `import.meta.env`.
- Run `npm run build` and inspect the generated `dist/` assets.

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

### Core Vue Concepts in SeniorMate

- **Component architecture:** App, views, and reusable components compose the
  interface.
- **Reactive state:** `ref` and `reactive` hold mutable UI/auth data.
- **Composition API:** `setup()` groups state, computed values, and actions.
- **Computed state:** Navigation and display values derive from other state.
- **Lifecycle hooks:** `onMounted()` loads route data after mounting.
- **Routing:** Vue Router selects views and applies permission guards.
- **Services pattern:** Plain modules isolate API paths and HTTP details.

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

## What Is Vuetify?

Vuetify is a Vue component framework implementing Material Design-inspired
components and layout utilities. SeniorMate uses it to provide accessible,
consistent tables, forms, dialogs, navigation, cards, grids, and feedback
states without hand-building every interaction.

Why use a component framework:

- Shared visual and interaction conventions.
- Responsive grid and spacing utilities.
- Accessible component behavior as a starting point.
- Faster delivery for data-heavy administration screens.
- Central theme/default configuration.

SeniorMate examples:

| SeniorMate UI | Vuetify concept |
| --- | --- |
| Patient list | `v-data-table` |
| Patient form | `v-form`, `v-text-field`, `v-select`, `v-textarea` |
| Dashboard metrics | Cards and responsive grid |
| Sidebar | Navigation drawer and lists |
| Delete confirmation | Dialog and buttons |
| Status display | Chips |
| Loading/empty/error states | Skeletons, alerts, progress, reusable wrappers |

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

## SeniorMate-to-Vue Map

The repository uses JavaScript filenames rather than the illustrative `.vue`
or TypeScript names commonly seen in tutorials.

| SeniorMate component | Vue concept |
| --- | --- |
| `PatientListView.js` | Routed component/page |
| `DashboardView.js` | Routed component/page |
| `PatientAvatar.js` | Reusable component |
| `router.js` | Vue Router route table and guard |
| `services/patients.js` | Service/API client module |
| `auth.js` | Reactive module-level state |
| `onMounted(loadPatients)` | Lifecycle hook |
| `computed(...)` rows/navigation | Derived reactive state |
| `v-if="canCreatePatient()"` | Conditional rendering |
| `v-model="form.first_name"` | Two-way form binding |

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

## Understanding the Design

### Why Vue instead of React or Angular?

Vue gives SeniorMate a concise reactive model and component system with less
framework ceremony than Angular and fewer architectural choices to assemble
than a typical React stack. The tradeoff is a smaller hiring ecosystem than
React and fewer enforced application conventions than Angular.

### Why Vuetify instead of PrimeVue?

This is a comparison, not a documented historical selection process.

Vuetify fits because SeniorMate already uses Material Design icons, layout
utilities, data tables, forms, dialogs, and a centrally customized theme.
PrimeVue offers a broad component catalog and different theming model, but
switching would replace nearly every template and visual convention.

Tradeoff: Vuetify accelerates consistent administration UI, but contributes a
large CSS/JavaScript bundle and makes the product's components closely tied to
its APIs.

## Learning Resources

### Vue Beginner

- [Vue Interactive Tutorial](https://vuejs.org/tutorial/)
- [Vue Guide Introduction](https://vuejs.org/guide/introduction.html)
- [Essentials: Reactivity Fundamentals](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)

### Vue Intermediate

- [Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Reusable Composables](https://vuejs.org/guide/reusability/composables.html)
- [Vue Router Guide](https://router.vuejs.org/guide/)
- [Vue Testing Guide](https://vuejs.org/guide/scaling-up/testing.html)

### Official Documentation

- [Vue Documentation](https://vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Vuetify Documentation](https://vuetifyjs.com/)
- [Vite Documentation](https://vite.dev/)

## Suggested Vue and Vuetify Experiments

1. Add a computed patient display name and observe automatic UI updates.
2. Extract repeated loading/error logic into a small composable.
3. Add route metadata to a temporary learning route and test the guard.
4. Build a small Vuetify data table from static data before connecting an API.
5. Add a form field with `v-model`, local validation, and backend error
   display.
6. Change one Vuetify theme color in development and identify every surface it
   affects.
