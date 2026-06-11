# Frontend Architecture

The frontend is a Vue 3 application using Vuetify and Vite. Components are
defined in JavaScript modules with inline Vue templates.

## Main Areas

- `src/main.js`: application startup, branding, authentication, and Vuetify.
- `src/router.js`: routes and permission metadata.
- `src/auth.js`: Keycloak initialization, session state, and token refresh.
- `src/permission-policy.js`: role-to-permission mapping.
- `src/services/`: API clients grouped by domain.
- `src/views/`: pages for dashboard, records, notes, reports, settings, and
  administration.
- `src/components/`: reusable states, headers, dialogs, status, avatars, and
  print components.
- `src/styles/main.css`: shared layout, responsive, and print styling.

## Data Flow

Views call service modules, which route requests through the shared HTTP layer.
The HTTP layer refreshes the Keycloak token and adds bearer authorization.
Errors are converted to user-facing messages rather than exposing stack traces.

Branding loads before the main shell and updates Vuetify colors and display
identity. Route guards improve UX, while API authorization remains final.
