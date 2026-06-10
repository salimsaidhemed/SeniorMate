# SeniorMate Roadmap

This roadmap captures the early direction for SeniorMate. It is intentionally lightweight and should evolve as product decisions become clearer.

## Foundation

- Standardise repository documentation, contribution rules, changelog, and GitHub templates.
- Complete local development setup for backend, frontend, database, authentication, and object storage.
- Establish CI checks for backend, frontend, and Docker workflows.

## Core Application

- Build patient profile and demographics management.
- Add caregiver and nursing visit tracking.
- Implement clinical note workflows for aide notes and nursing progress notes.
- Add care plan and patient assessment workflows.

## Operations and Security

- Define authentication, authorization, organization branding, and default identity architecture (`feature/21-auth-branding-design`).
- Implement Keycloak/OIDC login, backend JWT validation, and role enforcement (`feature/22-keycloak-auth`).
- Add organization branding settings, logo management, color controls, and live preview (`feature/23-org-branding-ui`).
- Add secure document upload and storage through MinIO.
- Provide printable clinical documentation.
- Build dashboard and reporting views for operational oversight.

## Deployment

- Mature Docker Compose for local and small-site deployments.
- Prepare Kubernetes deployment documentation once service boundaries are stable.
