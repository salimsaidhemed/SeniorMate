# API Overview

The Flask API is available under `/api`.

## Interactive Documentation

- Swagger UI: `http://localhost:5001/api/docs`
- OpenAPI JSON: `http://localhost:5001/api/openapi.json`
- Health: `http://localhost:5001/api/health`

Swagger and health remain public. Other API groups require a Keycloak bearer
token when authentication is enabled.

## Major Endpoint Groups

- `/patients`
- `/visits`
- `/aide-notes`
- `/nurse-notes`
- `/assessments`
- `/medical-records`
- `/dashboard`
- `/reports`
- `/settings/branding`
- `/admin/users`

## Example

```bash
curl \
  -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5001/api/patients?page=1&per_page=10"
```

Successful JSON responses usually use:

```json
{
  "data": {},
  "message": "Operation completed successfully"
}
```

List endpoints add pagination metadata where applicable. Report endpoints
return summary, grouped, recent, and row data; add `format=csv` for export.

For endpoint-level payloads and validation, see
[API Design](../architecture/api-design.md).
