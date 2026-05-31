import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "./views/DashboardView.js";
import PatientDetailView from "./views/PatientDetailView.js";
import PatientFormView from "./views/PatientFormView.js";
import PatientListView from "./views/PatientListView.js";

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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
