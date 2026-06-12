---
title: Architecture
description: Understand how the SeniorMate Vue frontend, Flask API, PostgreSQL, MinIO, Keycloak, and Docker Compose services work together.
---

# Clear service boundaries

<p class="section-intro">SeniorMate uses familiar open-source components with deliberately simple responsibilities. The browser communicates with the Flask API and Keycloak; private data services remain behind the backend.</p>

<MermaidDiagram />

<div class="architecture-notes">
  <div>
    <strong>Frontend</strong>
    Vue 3, Vuetify, and Vite provide the responsive application and role-aware experience.
  </div>
  <div>
    <strong>Application API</strong>
    Flask owns domain behavior, validation, authorization, reporting, and storage access.
  </div>
  <div>
    <strong>Data services</strong>
    PostgreSQL stores structured records; MinIO stores private file bytes and images.
  </div>
  <div>
    <strong>Identity</strong>
    Keycloak owns login, sessions, users, identity claims, and realm roles.
  </div>
  <div>
    <strong>Local operations</strong>
    Docker Compose starts the complete development environment with explicit configuration.
  </div>
  <div>
    <strong>Delivery</strong>
    GitHub Actions validates backend, frontend, Docker builds, and this public website.
  </div>
</div>

## Data and security

- The frontend does not connect directly to PostgreSQL, MinIO, or the Keycloak Admin API.
- The backend validates JWT issuer, audience, signature, expiry, and required roles when authentication is enabled.
- Uploaded records, patient photos, and organization logos remain private in MinIO.
- Domain metadata and relationships stay in PostgreSQL.
- Frontend route guards improve usability; backend authorization remains the security boundary.

[Read the full architecture documentation](https://github.com/salimsaidhemed/SeniorMate/tree/main/docs/architecture)
