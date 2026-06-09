# SeniorMate UI Guidelines

SeniorMate uses Vuetify with a restrained healthcare administration theme. These conventions keep workflows familiar, readable, and consistent as the product grows.

## Layout

- Use the shared `page-shell` class for page width and responsive padding.
- Use `PageHeader` for list and dashboard page titles, descriptions, and primary actions.
- Keep page-level actions in the header and record-level actions in the relevant table row or detail section.
- Use `SectionCard` for clearly bounded groups of related information.

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
- Every icon-only action must have an accessible label.
- Prefer comfortable density and avoid adding low-priority columns that make the table difficult to scan.

## Forms

- Group related fields in cards with clear section titles.
- Keep required fields visibly labelled and show field-level validation messages near the input.
- Use two-column layouts only where they collapse cleanly at narrow widths.
- Keep cancel and save actions together at the end of the form.
