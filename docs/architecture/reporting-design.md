# Reporting Design

SeniorMate reporting provides operational summaries without introducing a
separate analytics database in the first implementation.

## Reports

- Patient census
- Visit activity
- Staff activity
- Assessment summary
- Medical records summary

## API Shape

Every report returns:

```json
{
  "data": {
    "summary": {},
    "groups": {},
    "recent": [],
    "rows": []
  },
  "message": "Report retrieved successfully"
}
```

- `summary` drives metric cards.
- `groups` supplies label/count chart data.
- `recent` supplies a small current-activity view.
- `rows` supplies the detailed table and CSV export.

## Filters and Export

Reports apply relevant date, patient, staff, visit type, record type, and
status filters. JSON remains default; `format=csv` exports the filtered rows.

## Authorization

All current roles receive `reports.read`. Frontend navigation and routes use
that permission, while the Flask API enforces it on every report request.

## Evolution

Current reports query transactional PostgreSQL data directly. Introduce
materialized views, background aggregation, or a separate analytics store only
when measured data volume or response time justifies the complexity.
