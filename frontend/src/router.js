import { createRouter, createWebHistory } from "vue-router";
import { authState, hasAnyRole, login } from "./auth.js";

import DashboardView from "./views/DashboardView.js";
import AssessmentDetailView from "./views/AssessmentDetailView.js";
import AssessmentFormView from "./views/AssessmentFormView.js";
import AssessmentPrintView from "./views/AssessmentPrintView.js";
import AideNoteDetailView from "./views/AideNoteDetailView.js";
import AideNoteFormView from "./views/AideNoteFormView.js";
import AideNoteListView from "./views/AideNoteListView.js";
import AideNotePrintView from "./views/AideNotePrintView.js";
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
    meta: { roles: ["admin", "manager", "nurse", "viewer"] },
  },
  {
    path: "/patients",
    name: "patients",
    component: PatientListView,
  },
  {
    path: "/patients/new",
    name: "patient-create",
    component: PatientFormView,
    props: { mode: "create" },
    meta: { roles: ["admin", "manager"] },
  },
  {
    path: "/patients/:id",
    name: "patient-detail",
    component: PatientDetailView,
    props: true,
  },
  {
    path: "/patients/:id/edit",
    name: "patient-edit",
    component: PatientFormView,
    props: { mode: "edit" },
    meta: { roles: ["admin", "manager"] },
  },
  {
    path: "/patients/:id/print",
    name: "patient-print",
    component: PatientPrintView,
    props: true,
  },
  {
    path: "/assessments/new",
    name: "assessment-create",
    component: AssessmentFormView,
    props: { mode: "create" },
    meta: { roles: ["admin", "manager", "nurse"] },
  },
  {
    path: "/assessments/:id",
    name: "assessment-detail",
    component: AssessmentDetailView,
    props: true,
  },
  {
    path: "/assessments/:id/edit",
    name: "assessment-edit",
    component: AssessmentFormView,
    props: { mode: "edit" },
    meta: { roles: ["admin", "manager", "nurse"] },
  },
  {
    path: "/assessments/:id/print",
    name: "assessment-print",
    component: AssessmentPrintView,
    props: true,
  },
  {
    path: "/visits",
    name: "visits",
    component: VisitListView,
  },
  {
    path: "/visits/new",
    name: "visit-create",
    component: VisitFormView,
    props: { mode: "create" },
    meta: { roles: ["admin", "manager", "nurse"] },
  },
  {
    path: "/visits/:id",
    name: "visit-detail",
    component: VisitDetailView,
    props: true,
  },
  {
    path: "/visits/:id/edit",
    name: "visit-edit",
    component: VisitFormView,
    props: { mode: "edit" },
    meta: { roles: ["admin", "manager", "nurse"] },
  },
  {
    path: "/visits/:id/print",
    name: "visit-print",
    component: VisitPrintView,
    props: true,
  },
  {
    path: "/aide-notes",
    name: "aide-notes",
    component: AideNoteListView,
  },
  {
    path: "/aide-notes/new",
    name: "aide-note-create",
    component: AideNoteFormView,
    props: { mode: "create" },
    meta: { roles: ["admin", "manager", "caregiver"] },
  },
  {
    path: "/aide-notes/:id",
    name: "aide-note-detail",
    component: AideNoteDetailView,
    props: true,
  },
  {
    path: "/aide-notes/:id/edit",
    name: "aide-note-edit",
    component: AideNoteFormView,
    props: { mode: "edit" },
    meta: { roles: ["admin", "manager", "caregiver"] },
  },
  {
    path: "/aide-notes/:id/print",
    name: "aide-note-print",
    component: AideNotePrintView,
    props: true,
  },
  {
    path: "/nurse-notes",
    name: "nurse-notes",
    component: NurseNoteListView,
  },
  {
    path: "/nurse-notes/new",
    name: "nurse-note-create",
    component: NurseNoteFormView,
    props: { mode: "create" },
    meta: { roles: ["admin", "manager", "nurse"] },
  },
  {
    path: "/nurse-notes/:id",
    name: "nurse-note-detail",
    component: NurseNoteDetailView,
    props: true,
  },
  {
    path: "/nurse-notes/:id/edit",
    name: "nurse-note-edit",
    component: NurseNoteFormView,
    props: { mode: "edit" },
    meta: { roles: ["admin", "manager", "nurse"] },
  },
  {
    path: "/nurse-notes/:id/print",
    name: "nurse-note-print",
    component: NurseNotePrintView,
    props: true,
  },
  {
    path: "/settings/branding",
    name: "branding-settings",
    component: BrandingSettingsView,
    meta: { roles: ["admin", "manager"] },
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
  if (!hasAnyRole(to.meta.roles || [])) {
    return to.name === "dashboard"
      ? { name: "patients" }
      : { name: "dashboard" };
  }
  return true;
});

export default router;
