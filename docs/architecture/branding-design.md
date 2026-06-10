# Organization Branding Design

## Status

SeniorMate now implements a single default organization branding record,
private logo storage, public pre-authentication branding delivery, and dynamic
frontend theme behavior. Full multi-organization branding remains future work.

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

## Data Model

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

The first implementation uses the singleton row with `id=1`. Logo metadata is
stored with the settings record while file bytes remain in MinIO. Color values
are normalized to uppercase six-digit hexadecimal values.

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
- Serve custom logos through the safe public backend preview endpoint without
  exposing the private object key.
- Validate MIME type, extension, file signature, and configured file size.
- Parse SVG XML and reject scripts, event handlers, foreign embedded content,
  data URLs, and external references.
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

The Care Cross Wordmark is now the bundled production fallback. A missing or
unavailable custom logo immediately falls back to this asset.

## Settings UI

`Settings → Branding` is available to administrators and managers. It includes:

- `Settings → Branding` navigation.
- Organization and app display name fields.
- Logo upload, preview, replacement, and deletion.
- Color pickers with validated hex inputs.
- Live desktop and login preview.
- Hex color validation.
- Save, custom-logo deletion, and reset-to-default actions backed by the
  branding API.
- Dynamic application of branding to navigation, login, and print surfaces.

## API

```text
GET    /api/settings/branding
PUT    /api/settings/branding
POST   /api/settings/branding/logo
DELETE /api/settings/branding/logo
GET    /api/public/branding
GET    /api/public/branding/logo
```

Authenticated users may read settings. Only `admin` and `manager` roles may
mutate settings or logos. The public endpoint returns resolved display values
and a backend preview URL only; it never returns private bucket details or
object keys.

## Login Branding

The frontend loads public branding before starting OIDC, which allows the
document title and post-login application shell to use organization branding.
The actual login form is hosted by Keycloak and is not customized by this
feature. A future Keycloak theme can consume the same approved identity without
changing SeniorMate's settings model.
