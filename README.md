# SeniorMate

SeniorMate is a lightweight caregiver and patient management system designed to help small care providers manage patient information and visits in a simple, structured, and secure way.

The project is being built incrementally as a real, shippable product using small, focused iterations.


## Vision

Provide a simple digital system that replaces fragmented workflows (paper, spreadsheets, notes) with a clean and usable caregiver experience.

SeniorMate focuses on:
- Simplicity over complexity
- Real usability over feature bloat
- Incremental delivery (MVP → expansion)

## Current Version: v1 (MVP)

### Scope

SeniorMate v1 delivers the **minimum usable workflow**:

- Secure login (Keycloak)
- Patient management
- Visit logging
- Basic dashboard

### Core User Flow

1. Caregiver logs in
2. Views dashboard
3. Creates a patient
4. Opens patient profile
5. Records a visit
6. Views patient visit history

If this flow works end-to-end, v1 is successful.

---

## Out of Scope (v1)

To maintain focus and ensure delivery, the following are intentionally excluded:

- File uploads / medical records
- Assessments and scoring
- Advanced analytics
- Notifications
- Complex role/permission systems
- External integrations
- Kubernetes deployment

These will be introduced in later versions.

---

## Roadmap

### v1 — Patient Registry & Visit Logging
- Authentication (Keycloak)
- Patient CRUD
- Visit tracking
- Basic dashboard

### v2 — Medical Records
- File uploads (MinIO)
- Patient attachments
- Visit documents

### v3 — Assessments & Analytics
- Assessment forms
- Scoring system
- Enhanced dashboard insights

---

## Architecture

### Backend
- Flask (REST API)

### Frontend
- Vue 3 + Vuetify

### Authentication
- Keycloak (OIDC)

### Database
- PostgreSQL

### File Storage (v2+)
- MinIO

### Deployment
- Docker Compose (local development)
- Kubernetes (future)

---

## Project Structure

```text
seniormate/
├── backend/        # Flask API
├── frontend/       # Vue + Vuetify app
├── infra/
│   ├── docker/     # Docker configs
│   └── keycloak/   # Realm configuration
├── docs/           # Project documentation
├── docker-compose.yml
├── .env.example
└── README.md
```
---

## Getting Started (Local Development)

### Prerequisites

- Docker
- Docker Compose

---

### 1. Clone the repository

```bash
git clone https://github.com/salimsaidhemed/SeniorMate
cd SeniorMate
```

### 2. Configure environment

```bash
cp .env.example .env
```
Edit values if needed.

### 3. Start the stack
```bash
docker compose up --build
```
### 4. Access Services

|Service|URL|
|------:|--:|
|Frontend|http://localhost:3000|
|Backend|http://localhost:5000|
|Keycloak|http://localhost:8080|

### 5. Authentication
SeniorMate uses Keycloak for authentication.
- OpenID Connect (OIDC)
- JWT-based API protection
- Frontend handles login redirect
- Backend validates access tokens

### 6. Development Principles
This project follows strict development discipline:

1. MVP First
Build the smallest usable version before expanding.

2. 20-Hour Rule
Each version should be achievable in ~20 hours.

3. No Scope Creep
If it’s not required for the current version → defer it.

4. Incremental Evolution
Each version adds value without breaking simplicity.

### 7. Definition of Done (v1)
v1 is complete when:
- A user can log in via Keycloak
- Patients can be created and edited
- Patient profiles can be viewed
- Visits can be recorded and listed
- Dashboard shows real data
- The system runs via Docker Compose
- A new developer can run the project using this README

### 8. Future Enhancements
- File uploads (MinIO)
- Assessments and scoring
- Reporting and analytics
- Multi-role support
- Notifications
- Mobile-friendly UX improvements

### 9. Contributing
This project is currently under active development.
Contributions, feedback, and ideas are welcome in future phases.

### 10. License
TBD





