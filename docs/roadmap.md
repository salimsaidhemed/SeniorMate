# SeniorMate Roadmap

The roadmap tracks stable milestones and the next product investments. Scope
may change as real deployments and user feedback clarify priorities.

## Completed

### v1.0.0 - Initial Public Release

- Repository standards, contribution workflow, CI, and local Docker stack
- Patient management and patient photos
- Caregiver and nursing visits
- Aide Notes and Nurse Notes
- Patient assessments
- Private medical records in MinIO
- Search, filtering, pagination, dashboard, reports, and CSV export
- Printable patient, visit, note, and assessment views
- Keycloak authentication and backend authorization
- Frontend role-aware navigation and actions
- Organization branding
- Admin user management
- Guarded fictional demo data
- Comprehensive user, admin, technical, deployment, and architecture docs

Release details: [SeniorMate 1.0.0](releases/v1.0.0.md).

## Upcoming

### GitHub Pages Website

- Public project overview
- Documentation entry point
- Release and demo information

### Audit Logging

- Actor, action, target, timestamp, and outcome recording
- Administrative and clinical activity review
- Retention and export policy

### Notifications

- In-app notification model
- Email/SMS provider architecture
- User preferences and delivery status

### Scheduling

- Recurring visits
- Calendar and assignment views
- Missed visit and conflict handling

### Multi-Tenant Organizations

- Organization model and organization-scoped domain records
- Group/claim-based organization context
- Per-organization branding, users, and data isolation

## Later Considerations

- Production deployment and Kubernetes guidance
- Advanced analytics and materialized reporting
- Server-side PDF generation and scheduled reports
- Audit/compliance hardening
- Broader frontend unit and end-to-end testing
