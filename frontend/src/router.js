import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "./views/DashboardView.js";
import PatientDetailView from "./views/PatientDetailView.js";
import PatientFormView from "./views/PatientFormView.js";
import PatientListView from "./views/PatientListView.js";
import VisitDetailView from "./views/VisitDetailView.js";
import VisitFormView from "./views/VisitFormView.js";
import VisitListView from "./views/VisitListView.js";

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: DashboardView,
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
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
