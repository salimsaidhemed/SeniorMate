# Administrator Roles and Permissions

SeniorMate uses five roles:

- `admin`
- `manager`
- `nurse`
- `caregiver`
- `viewer`

Use the least-privileged role that supports the person's work. Multiple roles
combine permissions, so assign more than one only when there is a documented
need.

## Role Summary

- **Admin**: full application access, user administration, and branding.
- **Manager**: operational and clinical management plus branding.
- **Nurse**: patient read access and nursing, visit, assessment, and
  medical-record workflows.
- **Caregiver**: patient and visit read access plus Aide Note workflows.
- **Viewer**: read-only records and reports.

The detailed matrix is maintained in
[Roles and Permissions](../user-guide/roles-and-permissions.md).

## Security Boundary

Hidden links and buttons improve usability but do not grant or deny security.
The Flask API validates the token and permission on every protected request.
Test role changes by signing out and back in so a fresh token includes them.
