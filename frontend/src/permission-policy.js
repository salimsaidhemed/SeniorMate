export const ROLE_PERMISSIONS = {
  admin: ["*"],
  manager: [
    "patients.read",
    "patients.write",
    "visits.read",
    "visits.write",
    "aide_notes.read",
    "aide_notes.write",
    "nurse_notes.read",
    "nurse_notes.write",
    "assessments.read",
    "assessments.write",
    "medical_records.read",
    "medical_records.write",
    "patient_photos.read",
    "patient_photos.write",
    "patient_photos.verify",
    "dashboard.read",
    "reports.read",
    "branding.read",
    "branding.write",
  ],
  nurse: [
    "patients.read",
    "visits.read",
    "visits.write",
    "aide_notes.read",
    "nurse_notes.read",
    "nurse_notes.write",
    "assessments.read",
    "assessments.write",
    "medical_records.read",
    "medical_records.write",
    "patient_photos.read",
    "dashboard.read",
    "reports.read",
    "branding.read",
  ],
  caregiver: [
    "patients.read",
    "visits.read",
    "aide_notes.read",
    "aide_notes.write",
    "nurse_notes.read",
    "assessments.read",
    "medical_records.read",
    "patient_photos.read",
    "reports.read",
    "branding.read",
  ],
  viewer: [
    "patients.read",
    "visits.read",
    "aide_notes.read",
    "nurse_notes.read",
    "assessments.read",
    "medical_records.read",
    "patient_photos.read",
    "dashboard.read",
    "reports.read",
    "branding.read",
  ],
};

export function permissionsForRoles(roles = []) {
  const permissions = new Set();
  for (const role of roles) {
    for (const permission of ROLE_PERMISSIONS[role] || []) {
      permissions.add(permission);
    }
  }
  return permissions;
}

export function rolesCan(roles, permission) {
  const permissions = permissionsForRoles(roles);
  return permissions.has("*") || permissions.has(permission);
}
