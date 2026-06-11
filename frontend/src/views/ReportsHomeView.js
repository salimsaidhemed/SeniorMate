const reports = [
  {
    title: "Patient Census",
    description: "Patient status, demographics, diagnoses, and recent additions.",
    icon: "mdi-account-group-outline",
    to: "/reports/patient-census",
  },
  {
    title: "Visit Activity",
    description: "Visit volume, completion, cancellations, types, and trends.",
    icon: "mdi-calendar-chart-outline",
    to: "/reports/visit-activity",
  },
  {
    title: "Staff Activity",
    description: "Visits, care notes, and assessments completed by staff.",
    icon: "mdi-account-hard-hat-outline",
    to: "/reports/staff-activity",
  },
  {
    title: "Assessment Summary",
    description: "Assessment mix, completion status, and visit linkage.",
    icon: "mdi-clipboard-text-search-outline",
    to: "/reports/assessment-summary",
  },
  {
    title: "Medical Records Summary",
    description: "Document types, upload activity, and patient coverage.",
    icon: "mdi-file-chart-outline",
    to: "/reports/medical-records-summary",
  },
];


export default {
  setup() {
    return { reports };
  },
  template: `
    <div class="page-shell">
      <PageHeader
        title="Reports"
        subtitle="Operational views for census, care delivery, staff activity, and clinical documentation."
        icon="mdi-chart-box-outline"
      />

      <v-row>
        <v-col
          v-for="report in reports"
          :key="report.to"
          cols="12"
          md="6"
          lg="4"
        >
          <v-card class="section-card fill-height">
            <v-card-text class="pa-6">
              <v-icon :icon="report.icon" color="primary" size="32" class="mb-4" />
              <h2 class="text-h6 font-weight-bold mb-2">{{ report.title }}</h2>
              <p class="text-body-2 text-medium-emphasis mb-5">
                {{ report.description }}
              </p>
              <v-btn
                color="primary"
                variant="tonal"
                append-icon="mdi-arrow-right"
                :to="report.to"
              >
                Open report
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  `,
};
