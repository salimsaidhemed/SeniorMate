# Reports

SeniorMate reports turn patient, visit, staff, assessment, and medical-record
activity into operational views for administrators, managers, nurses,
caregivers, and viewers.

Open **Reports** from the main navigation. Every SeniorMate role currently has
`reports.read`; backend authorization remains authoritative.

## Available Reports

### Patient Census

Shows total, active, and inactive patients, demographics, diagnosis groupings,
and recently added patients.

### Visit Activity

Shows visit totals, completion and cancellation counts, visit types, staff
roles, daily activity, and detailed visit rows.

### Staff Activity

Summarizes visits, aide notes, nurse notes, and completed assessments by staff
member.

### Assessment Summary

Shows assessment type and status distributions, recent assessments, and how
many assessments are linked to visits.

### Medical Records Summary

Shows document types, upload dates, recent uploads, and how many patients have
medical records.

## Filters

Reports expose only relevant filters from:

- Start and end date.
- Patient ID.
- Staff role and staff name.
- Visit type.
- Status.
- Record type on the Medical Records Summary.

Select **Apply filters** to refresh the report. **Clear filters** returns to the
complete dataset. Empty results display a normal empty state rather than an
error.

## CSV Export

Select **Export CSV** to download the detailed rows for the current report and
active filters. JSON remains the API default. CSV exports contain tabular
records, while summary cards and grouped chart data remain available in JSON.

CSV files contain fictional data when used with the guarded demo seed from
[Demo Data](../setup/demo-data.md). Review exports before sharing them outside
the local environment.
