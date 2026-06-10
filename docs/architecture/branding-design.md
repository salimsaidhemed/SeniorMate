# Organization Branding Design

## Status

This document defines the future SeniorMate branding architecture. It does not add database models, settings APIs, uploads, or dynamic theme behavior.

## Goals

- Preserve a professional SeniorMate identity by default.
- Allow each organization to apply restrained, accessible branding.
- Keep clinical and administrative workflows visually predictable.
- Make missing or incomplete configuration safe through deterministic fallbacks.
- Store private uploaded logos in MinIO rather than PostgreSQL.

## Configurable Branding

Future organization branding may configure:

| Setting | Purpose |
| --- | --- |
| `organization_name` | Legal or operational organization name. |
| `app_display_name` | Product name shown in navigation and login surfaces. |
| `logo_object_key` | Private MinIO object key for the organization logo. |
| `primary_color` | Primary actions, links, and active navigation. |
| `secondary_color` | Supporting actions and operational information. |
| `accent_color` | Limited highlights and selected emphasis. |
| `sidebar_color` | Navigation background where contrast remains accessible. |
| `login_banner_text` | Short organization-approved login message. |
| `footer_text` | Organization or deployment footer text. |

Branding should not permit arbitrary CSS, HTML, scripts, remote image URLs, or font uploads in the first implementation.

## Fallback Behavior

Branding must resolve each field independently:

1. Use a valid organization setting when present.
2. Otherwise use the SeniorMate default for that field.

Required defaults:

- Use the default SeniorMate logo when no custom logo exists or the stored object cannot be loaded.
- Use `SeniorMate` when no custom app display name exists.
- Use the existing SeniorMate Vuetify theme when colors are absent, malformed, or fail validation.
- Use the organization name only where configured; do not expose internal slugs as display names.
- Hide optional login banner and footer text when empty.

The application must never show a broken image icon. Logo loading should fall back to the bundled default asset.

## Proposed Data Model

This is a future model proposal, not an implementation.

### OrganizationSettings

```text
id
organization_name
app_display_name
logo_object_key
primary_color
secondary_color
accent_color
sidebar_color
login_banner_text
footer_text
created_at
updated_at
```

An organization should have at most one active settings record. Color values should be normalized to six-digit hexadecimal values and validated for acceptable contrast before saving.

### Optional Organization

```text
id
name
slug
status
created_at
updated_at
```

When multi-organization support is introduced, `OrganizationSettings` should reference `organization_id` rather than relying on a global singleton.

## Storage and Delivery

- Store uploaded logo binaries in a private MinIO bucket.
- Store only object keys and metadata in PostgreSQL.
- Serve logos through an authenticated backend endpoint or short-lived presigned URL.
- Validate MIME type, file signature, dimensions, and file size.
- Initially accept SVG only if it is sanitized safely; otherwise limit uploads to PNG and JPEG.
- Cache resolved branding in the frontend with a clear invalidation strategy after settings updates.

Bundled SeniorMate default assets remain part of the frontend build and require no storage service.

## Theme Application

The frontend should resolve a branding configuration before rendering the authenticated application shell. Valid colors can then extend the existing Vuetify theme.

Accessibility constraints:

- Maintain WCAG AA contrast for normal navigation and button text.
- Reject or replace unsafe color combinations.
- Keep error, warning, success, and clinical status colors semantically stable.
- Do not let organization branding obscure focus states or validation messages.

Brand colors should personalize the shell without recoloring every clinical status or data visualization.

## Default Logo Concepts

Four original vector concepts are available under:

`frontend/src/assets/branding/logo-concepts/`

1. **Care Cross Wordmark**: a soft cross assembled from balanced rounded blocks beside the SeniorMate name.
2. **SM Path Monogram**: compact initials connected by a care-path line for small navigation surfaces.
3. **Care Shield**: a protective shield with a centered care cross for trust and clinical administration.
4. **Heart at Home**: an abstract home roof and heart line representing care delivered where people live.

### Recommended Default

**Care Cross Wordmark** is the recommended initial SeniorMate default.

It is the clearest at first glance, works in healthcare and administrative contexts without feeling institutional, and separates cleanly into a square mark and horizontal wordmark. Its simple geometry remains legible at sidebar, favicon, login, print, and document-header sizes. The recommendation is intentionally easy to override after maintainer review.

No concept is wired into the production app by this feature.

## Future Settings UI

A later feature should implement:

- `Settings → Branding` navigation.
- Organization and app display name fields.
- Logo upload, preview, replacement, and deletion.
- Color pickers with validated hex inputs.
- Live desktop and login preview.
- Accessible contrast warnings.
- Save/reset actions backed by a settings API.
- Dynamic application of branding to navigation, login, and print surfaces.

## API Direction

Potential future endpoints:

```text
GET    /api/organization/settings
PUT    /api/organization/settings
POST   /api/organization/settings/logo
GET    /api/organization/settings/logo
DELETE /api/organization/settings/logo
```

Only users with `branding.manage` should mutate settings. A public or pre-authentication branding endpoint may later expose a deliberately limited, non-sensitive subset for the login screen.

