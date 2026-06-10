# SeniorMate UI Guidelines

SeniorMate uses Vuetify with a restrained healthcare administration theme. These conventions keep workflows familiar, readable, and consistent as the product grows.

## Layout

- Use the shared `page-shell` class for page width and responsive padding.
- Use `PageHeader` for list and dashboard page titles, descriptions, and primary actions.
- Use `DetailHeader` for patient, visit, note, and assessment identity, status, and record actions.
- Keep page-level actions in the header and record-level actions in the relevant table row or detail section.
- Use `SectionCard` for clearly bounded groups of related information.
- Use tabs when a detail page contains several independent record collections. Keep overview information first and operational records in a predictable order.

## Color and Status

- Primary teal identifies main actions and active navigation.
- Secondary blue-grey supports neutral operational information.
- Green represents active or completed states.
- Muted grey represents inactive or cancelled states.
- Red is reserved for errors and destructive actions.
- Use `StatusChip` rather than defining status colors in individual pages.

## Feedback States

- Use `LoadingState` while list or page data is loading.
- Use `EmptyState` when a workflow has no records yet.
- Use `ErrorAlert` for user-facing request failures.
- Use `ConfirmDialog` before destructive actions.
- Success messages should be concise and describe the completed action.

## Tables

- Keep action icons together at the end of each row.
- Every icon-only action must have an accessible label and a visible browser tooltip.
- Prefer comfortable density and avoid adding low-priority columns that make the table difficult to scan.
- Use `StatusChip` for record state and `EmptyState` inside the table when no rows exist.

## Forms

- Group related fields in cards with clear section titles.
- Keep required fields visibly labelled and show field-level validation messages near the input.
- Use two-column layouts only where they collapse cleanly at narrow widths.
- Keep cancel and save actions together at the end of the form.
- Put cancel before the primary save action and use the same `form-actions` layout across forms.

## Detail Pages

- Lead with identity and care context before metadata.
- Keep the most common action visible and move secondary actions into the relevant section.
- Group visit documentation actions together so note and assessment status can be scanned quickly.
- Avoid stacking unrelated data sections into one continuous page when tabs provide clearer navigation.

## Print Views

- Print reports should use a dedicated print layout with navigation and interactive controls hidden.
- Use plain white backgrounds, dark text, restrained borders, and page-safe spacing.
- Render checklist and JSON-backed clinical data as readable labels rather than raw JSON.
- Use the patient photo when available and the shared initials fallback otherwise.
