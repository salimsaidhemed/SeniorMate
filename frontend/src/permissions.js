import { authState } from "./auth.js";
import {
  permissionsForRoles,
  rolesCan,
} from "./permission-policy.js";

export { ROLE_PERMISSIONS, permissionsForRoles } from "./permission-policy.js";

function activeRoles(roles) {
  return roles || authState.roles;
}

export function hasRole(role, roles) {
  return activeRoles(roles).includes(role);
}

export function hasAnyRole(roles, userRoles) {
  return roles.length === 0
    || roles.some((role) => activeRoles(userRoles).includes(role));
}

export function can(permission, roles) {
  return rolesCan(activeRoles(roles), permission);
}

export function canAny(permissions, roles) {
  return permissions.some((permission) => can(permission, roles));
}

export const canManagePatients = (roles) => can("patients.write", roles);
export const canCreatePatient = canManagePatients;
export const canEditPatient = canManagePatients;
export const canDeletePatient = canManagePatients;
export const canManageVisits = (roles) => can("visits.write", roles);
export const canCreateAideNote = (roles) => can("aide_notes.write", roles);
export const canCreateNurseNote = (roles) => can("nurse_notes.write", roles);
export const canManageAssessments = (roles) => can("assessments.write", roles);
export const canManageMedicalRecords = (roles) =>
  can("medical_records.write", roles);
export const canManagePatientPhotos = (roles) =>
  can("patient_photos.write", roles);
export const canVerifyPatientPhoto = (roles) =>
  can("patient_photos.verify", roles);
export const canManageBranding = (roles) => can("branding.write", roles);
export const canManageUsers = (roles) => can("user_admin.manage", roles);
export const canViewReports = (roles) => can("reports.read", roles);
export const canViewDashboard = (roles) => can("dashboard.read", roles);
