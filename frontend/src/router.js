import { createRouter, createWebHistory } from "vue-router";
import { authState, login } from "./auth.js";
import { can } from "./permissions.js";

import AccessDeniedView from "./views/AccessDeniedView.js";
import DashboardView from "./views/DashboardView.js";
import AssessmentDetailView from "./views/AssessmentDetailView.js";
import AssessmentFormView from "./views/AssessmentFormView.js";
import AssessmentPrintView from "./views/AssessmentPrintView.js";
import AideNoteDetailView from "./views/AideNoteDetailView.js";
import AideNoteFormView from "./views/AideNoteFormView.js";
import AideNoteListView from "./views/AideNoteListView.js";
import AideNotePrintView from "./views/AideNotePrintView.js";
import AdminUsersView from "./views/AdminUsersView.js";
import BrandingSettingsView from "./views/BrandingSettingsView.js";
import NurseNotePrintView from "./views/NurseNotePrintView.js";
import PatientDetailView from "./views/PatientDetailView.js";
import PatientFormView from "./views/PatientFormView.js";
import PatientListView from "./views/PatientListView.js";
import PatientPrintView from "./views/PatientPrintView.js";
import NurseNoteDetailView from "./views/NurseNoteDetailView.js";
import NurseNoteFormView from "./views/NurseNoteFormView.js";
import NurseNoteListView from "./views/NurseNoteListView.js";
import VisitDetailView from "./views/VisitDetailView.js";
import VisitFormView from "./views/VisitFormView.js";
import VisitListView from "./views/VisitListView.js";
import VisitPrintView from "./views/VisitPrintView.js";

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: DashboardView,
    meta: { permission: "dashboard.read" },
  },
  {
    path: "/patients",
    name: "patients",
    component: PatientListView,
    meta: { permission: "patients.read" },
  },
  {
    path: "/patients/new",
    name: "patient-create",
    component: PatientFormView,
    props: { mode: "create" },
    meta: { permission: "patients.write" },
  },
  {
    path: "/patients/:id",
    name: "patient-detail",
    component: PatientDetailView,
    props: true,
    meta: { permission: "patients.read" },
  },
  {
    path: "/patients/:id/edit",
    name: "patient-edit",
    component: PatientFormView,
    props: { mode: "edit" },
    meta: { permission: "patients.write" },
  },
  {
    path: "/patients/:id/print",
    name: "patient-print",
    component: PatientPrintView,
    props: true,
    meta: { permission: "reports.read" },
  },
  {
    path: "/assessments/new",
    name: "assessment-create",
    component: AssessmentFormView,
    props: { mode: "create" },
    meta: { permission: "assessments.write" },
  },
  {
    path: "/assessments/:id",
    name: "assessment-detail",
    component: AssessmentDetailView,
    props: true,
    meta: { permission: "assessments.read" },
  },
  {
    path: "/assessments/:id/edit",
    name: "assessment-edit",
    component: AssessmentFormView,
    props: { mode: "edit" },
    meta: { permission: "assessments.write" },
  },
  {
    path: "/assessments/:id/print",
    name: "assessment-print",
    component: AssessmentPrintView,
    props: true,
    meta: { permission: "reports.read" },
  },
  {
    path: "/visits",
    name: "visits",
    component: VisitListView,
    meta: { permission: "visits.read" },
  },
  {
    path: "/visits/new",
    name: "visit-create",
    component: VisitFormView,
    props: { mode: "create" },
    meta: { permission: "visits.write" },
  },
  {
    path: "/visits/:id",
    name: "visit-detail",
    component: VisitDetailView,
    props: true,
    meta: { permission: "visits.read" },
  },
  {
    path: "/visits/:id/edit",
    name: "visit-edit",
    component: VisitFormView,
    props: { mode: "edit" },
    meta: { permission: "visits.write" },
  },
  {
    path: "/visits/:id/print",
    name: "visit-print",
    component: VisitPrintView,
    props: true,
    meta: { permission: "reports.read" },
  },
  {
    path: "/aide-notes",
    name: "aide-notes",
    component: AideNoteListView,
    meta: { permission: "aide_notes.read" },
  },
  {
    path: "/aide-notes/new",
    name: "aide-note-create",
    component: AideNoteFormView,
    props: { mode: "create" },
    meta: { permission: "aide_notes.write" },
  },
  {
    path: "/aide-notes/:id",
    name: "aide-note-detail",
    component: AideNoteDetailView,
    props: true,
    meta: { permission: "aide_notes.read" },
  },
  {
    path: "/aide-notes/:id/edit",
    name: "aide-note-edit",
    component: AideNoteFormView,
    props: { mode: "edit" },
    meta: { permission: "aide_notes.write" },
  },
  {
    path: "/aide-notes/:id/print",
    name: "aide-note-print",
    component: AideNotePrintView,
    props: true,
    meta: { permission: "reports.read" },
  },
  {
    path: "/nurse-notes",
    name: "nurse-notes",
    component: NurseNoteListView,
    meta: { permission: "nurse_notes.read" },
  },
  {
    path: "/nurse-notes/new",
    name: "nurse-note-create",
    component: NurseNoteFormView,
    props: { mode: "create" },
    meta: { permission: "nurse_notes.write" },
  },
  {
    path: "/nurse-notes/:id",
    name: "nurse-note-detail",
    component: NurseNoteDetailView,
    props: true,
    meta: { permission: "nurse_notes.read" },
  },
  {
    path: "/nurse-notes/:id/edit",
    name: "nurse-note-edit",
    component: NurseNoteFormView,
    props: { mode: "edit" },
    meta: { permission: "nurse_notes.write" },
  },
  {
    path: "/nurse-notes/:id/print",
    name: "nurse-note-print",
    component: NurseNotePrintView,
    props: true,
    meta: { permission: "reports.read" },
  },
  {
    path: "/admin/users",
    name: "admin-users",
    component: AdminUsersView,
    meta: { permission: "user_admin.manage" },
  },
  {
    path: "/settings/branding",
    name: "branding-settings",
    component: BrandingSettingsView,
    meta: { permission: "branding.write" },
  },
  {
    path: "/access-denied",
    name: "access-denied",
    component: AccessDeniedView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  if (authState.error) {
    return true;
  }
  if (!authState.authenticated) {
    await login();
    return false;
  }
  if (
    to.name !== "access-denied"
    && to.meta.permission
    && !can(to.meta.permission)
  ) {
    return {
      name: "access-denied",
      query: { from: to.fullPath },
    };
  }
  return true;
});

export default router;
