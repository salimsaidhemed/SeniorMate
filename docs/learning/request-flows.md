# SeniorMate Request Flows

These sequence diagrams show the major runtime boundaries. The exact UI
component varies, but the authentication, API, persistence, and storage paths
remain consistent.

## User Login

```mermaid
sequenceDiagram
    actor User
    participant Vue
    participant Keycloak
    participant API as Flask API

    User->>Vue: Open protected route
    Vue->>Keycloak: Authorization Code + PKCE login
    Keycloak-->>User: Login form
    User->>Keycloak: Submit credentials
    Keycloak-->>Vue: Authorization code
    Vue->>Keycloak: Exchange code + verifier
    Keycloak-->>Vue: Access token
    Vue->>API: GET /api/... + Bearer token
    API->>Keycloak: Fetch/cache JWKS signing key
    Keycloak-->>API: Public key
    API-->>Vue: Authorized JSON response
```

## Loading the Dashboard

```mermaid
sequenceDiagram
    actor User
    participant View as DashboardView
    participant Service as dashboard service
    participant API as Flask API
    participant DB as PostgreSQL

    User->>View: Open dashboard
    View->>Service: getDashboardStats()
    Service->>API: GET /api/dashboard/stats
    API->>API: Authenticate and require dashboard.read
    API->>DB: Count and group patients, visits, notes
    DB-->>API: Aggregates and recent visits
    API-->>Service: data + message
    Service-->>View: Parsed response
    View-->>User: Cards, charts, recent visits
```

## Creating a Patient

```mermaid
sequenceDiagram
    actor User
    participant Form as PatientFormView
    participant Service as patients service
    participant API as Patient route
    participant DB as PostgreSQL

    User->>Form: Enter details and save
    Form->>Form: Validate required names
    Form->>Service: createPatient(payload)
    Service->>API: POST /api/patients
    API->>API: Require patients.write
    API->>API: Parse and validate payload
    API->>DB: INSERT patient
    DB-->>API: Patient ID and timestamps
    API-->>Service: 201 patient response
    Service-->>Form: Created patient
    Form-->>User: Navigate to Patient Detail
```

## Uploading a Medical Record

```mermaid
sequenceDiagram
    actor User
    participant UI as MedicalRecordsSection
    participant API as Medical record route
    participant DB as PostgreSQL
    participant MinIO

    User->>UI: Select metadata and file
    UI->>API: POST multipart /api/medical-records
    API->>API: Validate patient, size, MIME, extension, signature
    API->>MinIO: Ensure bucket and upload object
    MinIO-->>API: Upload complete
    API->>DB: INSERT metadata + object key
    alt Database commit succeeds
        DB-->>API: Record persisted
        API-->>UI: 201 record response
    else Database commit fails
        API->>MinIO: Delete uploaded object
        API-->>UI: Error
    end
```

## Uploading a Patient Photo

```mermaid
sequenceDiagram
    actor User
    participant Detail as PatientDetailView
    participant API as Patient photo route
    participant DB as PostgreSQL
    participant MinIO

    User->>Detail: Choose JPEG/PNG
    Detail->>API: POST /api/patients/:id/photo
    API->>API: Validate file type, signature, and size
    API->>MinIO: Upload new profile object
    API->>DB: Save photo metadata, verified=false
    DB-->>API: Commit
    opt Previous photo existed
        API->>MinIO: Delete previous object
    end
    API-->>Detail: Updated patient metadata
    Detail-->>User: Refresh avatar and review status
```

## Creating an Aide Note

```mermaid
sequenceDiagram
    actor Caregiver
    participant Form as AideNoteFormView
    participant API as Aide note route
    participant DB as PostgreSQL

    Caregiver->>Form: Complete checklist and staff details
    Form->>API: POST /api/aide-notes
    API->>API: Require aide_notes.write
    API->>DB: Find patient and visit
    DB-->>API: Related records
    API->>API: Confirm visit belongs to patient
    API->>DB: Check note does not already exist
    API->>DB: INSERT AideNote JSON + text fields
    DB-->>API: Created note
    API-->>Form: 201 response
    Form-->>Caregiver: Navigate to note detail
```

## Creating a Nurse Note

```mermaid
sequenceDiagram
    actor Nurse
    participant Form as NurseNoteFormView
    participant API as Nurse note route
    participant DB as PostgreSQL

    Nurse->>Form: Complete clinical sections
    Form->>API: POST /api/nurse-notes
    API->>API: Require nurse_notes.write
    API->>DB: Validate patient and visit relationship
    API->>DB: Check one-note-per-visit constraint
    API->>API: Validate JSON clinical sections
    API->>DB: INSERT NurseNote
    DB-->>API: Created note
    API-->>Form: 201 response
    Form-->>Nurse: Navigate to note detail
```

## Generating a Report

```mermaid
sequenceDiagram
    actor User
    participant View as ReportDetailView
    participant Service as reports service
    participant API as Report route
    participant DB as PostgreSQL

    User->>View: Choose report and filters
    View->>Service: getReport(key, filters)
    Service->>API: GET /api/reports/...?...filters
    API->>API: Require reports.read and validate filters
    API->>DB: Query and aggregate records
    DB-->>API: Filtered rows
    API-->>Service: Summary, groups, recent, rows
    Service-->>View: Report data
    View-->>User: Summary cards, chart, table
    opt Export CSV
        User->>Service: Request format=csv
        Service->>API: GET report?format=csv
        API-->>User: text/csv download
    end
```
