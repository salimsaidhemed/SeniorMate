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

The repository is currently a scaffold. Use these steps as the standard local setup flow as backend, frontend, and Docker services are implemented.

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

5. Start services when Docker Compose services are populated.

   ```bash
   cd ..
   docker compose up --build
   ```

## Development Workflow

- Start new work from an up-to-date `main` branch.
- Create a focused feature or fix branch.
- Keep documentation and `CHANGELOG.md` updated with user-facing or workflow changes.
- Open a pull request using the repository template.
- Do not merge your own pull request. Only the maintainer merges into `main`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution process.
