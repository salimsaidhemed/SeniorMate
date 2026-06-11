# SeniorMate

SeniorMate is a caregiver and patient management platform for home healthcare agencies, adult day care centers, assisted living facilities, and independent caregivers.

The project is intended to centralize patient records, caregiver visits, nursing assessments, care plans, clinical documentation, secure document storage, and operational reporting. SeniorMate is currently in early repository setup, with the project structure and contribution workflow being standardised before feature development begins.

## Planned Features

- Patient profile and demographics management
- Caregiver and nursing visit tracking
- Digital aide notes and nursing progress notes
- Medical record and document management
- Patient assessments and care plans
- Dashboard and operational analytics
- Role-based access control
- Printable clinical documentation
- Secure file storage
- Docker-based local and deployment workflows

## Technology Stack

- Backend: Python, Flask
- Frontend: Vue 3, Vuetify, Vite
- Database: PostgreSQL
- Authentication: Keycloak
- Object storage: MinIO
- Deployment: Docker, Docker Compose, Kubernetes-ready structure
- CI/CD: GitHub Actions

## Project Structure

```text
SeniorMate/
├── backend/                 # Flask backend application scaffold
│   ├── app/                 # Backend package
│   ├── requirements.txt     # Runtime Python dependencies
│   └── requirements-dev.txt # Development Python dependencies
├── frontend/                # Vue frontend application scaffold
│   └── src/                 # Frontend source files
├── docs/                    # Project documentation
├── .github/                 # GitHub templates, workflows, and ownership rules
├── docker-compose.yml       # Local service orchestration scaffold
├── .env.example             # Safe local environment template
├── CHANGELOG.md             # Project change history
└── CONTRIBUTING.md          # Contribution workflow
```

## Local Development

Docker Compose is the recommended way to run the local SeniorMate stack. It starts the Flask backend, Vue/Vite frontend, PostgreSQL, and MinIO with safe local defaults from `.env.example`. Keycloak can be enabled through the `auth` profile.

### Prerequisites

- Git
- Python 3.11 or newer
- Node.js 20 or newer
- Docker and Docker Compose

### Setup

1. Clone the repository.

   ```bash
   git clone git@github.com:salimsaidhemed/SeniorMate.git
   cd SeniorMate
   ```

2. Create your local environment file.

   ```bash
   cp .env.example .env
   ```

3. Prepare the backend environment.

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   ```

4. Prepare the frontend environment.

   ```bash
   cd ../frontend
   npm install
   ```

5. Start the local stack.

   ```bash
   cd ..
   docker compose up --build
   ```

6. Open the local services.

   - Frontend: `http://localhost:5173`
   - Dashboard: `http://localhost:5173`
   - Patient management UI: `http://localhost:5173/patients`
   - Visits UI: `http://localhost:5173/visits`
   - Aide Notes UI: `http://localhost:5173/aide-notes`
   - Nurse Notes UI: `http://localhost:5173/nurse-notes`
   - Admin user management: `http://localhost:5173/admin/users`
   - Branding settings: `http://localhost:5173/settings/branding`
   - Backend health: `http://localhost:5001/api/health`
   - Swagger UI: `http://localhost:5001/api/docs`
   - OpenAPI JSON: `http://localhost:5001/api/openapi.json`
   - MinIO console: `http://localhost:9001`
   - PostgreSQL: `localhost:5432`

Authentication and Keycloak are enabled by default. Start the complete local
stack, including the imported development realm, with:

```bash
docker compose up --build
```

Keycloak runs at `http://localhost:8080`. SeniorMate uses Authorization Code
with PKCE in the frontend and validates signed access tokens, issuer, audience,
and expiry in the backend. See
[docs/setup/keycloak-local-setup.md](docs/setup/keycloak-local-setup.md) for
the imported realm, local demo users, roles, and Swagger testing workflow.

For a temporary unauthenticated development session, set both
`AUTH_ENABLED=false` and `VITE_AUTH_ENABLED=false`. Automated backend tests
continue to disable authentication explicitly.

Optional fictional demo records can be created through guarded Flask CLI
commands. Demo seeding is disabled by default and never runs at startup. See
[docs/setup/demo-data.md](docs/setup/demo-data.md) for enablement, seed, reset,
and safety instructions.

Administrators and managers can customize the app and organization names,
logo, theme colors, banner text, and footer text from `Settings → Branding`.
Custom logos remain private in MinIO and are delivered through the backend.

When authentication is enabled, administrators can manage Keycloak users,
temporary password resets, enabled status, and SeniorMate roles from
`Admin → Users`. See
[docs/user-guide/admin-user-management.md](docs/user-guide/admin-user-management.md)
for the workflow and safety constraints.

## CI Checks

GitHub Actions runs basic checks on pull requests and pushes to `main`:

- Backend CI installs Python dependencies, runs Ruff, and executes pytest.
- Frontend CI installs Node dependencies from the lockfile and runs the Vite build.
- Docker Build validates the Compose file and builds the backend and frontend images without pushing them.

## Printable Reports

Print-friendly reports are available from the detail pages for patients,
visits, aide notes, nurse notes, and patient assessments. Use the report's
`Print / Save PDF` action to open the browser print dialog, then select a
printer or choose the browser's PDF destination.

Printable patient summaries include recent visits, assessments, and medical
record metadata. Uploaded medical record files are referenced by name and are
not embedded in reports.

Operational analytics are available from the Reports section with patient
census, visit activity, staff activity, assessment, and medical-record views.
Each report supports relevant filters and CSV export. See
[docs/user-guide/reports.md](docs/user-guide/reports.md).

## Development Workflow

- Start new work from an up-to-date `main` branch.
- Create a focused feature or fix branch.
- Keep documentation and `CHANGELOG.md` updated with user-facing or workflow changes.
- Open a pull request using the repository template.
- Do not merge your own pull request. Only the maintainer merges into `main`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution process.
