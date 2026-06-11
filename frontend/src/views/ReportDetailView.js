import { computed, onMounted, reactive, ref, watch } from "vue";

import { exportReportCsv, getReport } from "../services/reports.js";


const commonDateFilters = ["start_date", "end_date"];

const configurations = {
  "patient-census": {
    title: "Patient Census",
    subtitle: "Patient population, status, demographics, and diagnoses.",
    icon: "mdi-account-group-outline",
    filters: [...commonDateFilters, "patient_id", "status"],
    statuses: ["active", "inactive"],
    summaryLabels: {
      total_patients: "Total patients",
      active_patients: "Active patients",
      inactive_patients: "Inactive patients",
    },
    groupLabels: {
      patients_by_gender: "Patients by gender",
      patients_by_diagnosis: "Patients by diagnosis",
    },
    headers: [
      { title: "Patient", key: "patient_name" },
      { title: "Status", key: "status" },
      { title: "Gender", key: "gender" },
      { title: "Date of birth", key: "date_of_birth" },
      { title: "Diagnosis", key: "diagnosis" },
      { title: "Added", key: "created_at" },
    ],
  },
  "visit-activity": {
    title: "Visit Activity",
    subtitle: "Care delivery volume, completion, cancellations, and trends.",
    icon: "mdi-calendar-chart-outline",
    filters: [
      ...commonDateFilters,
      "patient_id",
      "staff_role",
      "staff_name",
      "visit_type",
      "status",
    ],
    statuses: ["scheduled", "completed", "cancelled"],
    summaryLabels: {
      total_visits: "Total visits",
      completed_visits: "Completed",
      scheduled_visits: "Scheduled",
      cancelled_visits: "Cancelled",
    },
    groupLabels: {
      visits_by_type: "Visits by type",
      visits_by_status: "Visits by status",
      visits_by_staff_role: "Visits by staff role",
      visits_over_time: "Visits over time",
    },
    headers: [
      { title: "Patient", key: "patient_name" },
      { title: "Date", key: "visit_date" },
      { title: "Visit type", key: "visit_type" },
      { title: "Staff", key: "staff_name" },
      { title: "Role", key: "staff_role" },
      { title: "Status", key: "status" },
    ],
  },
  "staff-activity": {
    title: "Staff Activity",
    subtitle: "Visits, care notes, and assessments completed by staff.",
    icon: "mdi-account-hard-hat-outline",
    filters: [
      ...commonDateFilters,
      "patient_id",
      "staff_role",
      "staff_name",
      "visit_type",
      "status",
    ],
    statuses: ["scheduled", "completed", "cancelled"],
    summaryLabels: {
      total_staff: "Staff represented",
      total_visits: "Total visits",
      total_notes: "Care notes",
      total_assessments: "Assessments",
    },
    groupLabels: { activity_by_role: "Visits by staff role" },
    headers: [
      { title: "Staff", key: "staff_name" },
      { title: "Role", key: "staff_role" },
      { title: "Visits", key: "total_visits" },
      { title: "Aide notes", key: "aide_notes_completed" },
      { title: "Nurse notes", key: "nurse_notes_completed" },
      { title: "Assessments", key: "assessments_completed" },
    ],
  },
  "assessment-summary": {
    title: "Assessment Summary",
    subtitle: "Assessment mix, completion, and linkage to care visits.",
    icon: "mdi-clipboard-text-search-outline",
    filters: [...commonDateFilters, "patient_id", "status"],
    statuses: ["draft", "completed"],
    summaryLabels: {
      total_assessments: "Total assessments",
      completed_assessments: "Completed",
      draft_assessments: "Draft",
      linked_to_visits: "Linked to visits",
    },
    groupLabels: {
      assessments_by_type: "Assessments by type",
      assessments_by_status: "Assessments by status",
    },
    headers: [
      { title: "Patient", key: "patient_name" },
      { title: "Date", key: "assessment_date" },
      { title: "Type", key: "assessment_type" },
      { title: "Status", key: "status" },
      { title: "Performed by", key: "performed_by" },
      { title: "Linked visit", key: "linked_visit" },
    ],
  },
  "medical-records-summary": {
    title: "Medical Records Summary",
    subtitle: "Document coverage, types, and upload activity.",
    icon: "mdi-file-chart-outline",
    filters: [...commonDateFilters, "patient_id", "visit_type"],
    summaryLabels: {
      total_records: "Total records",
      patients_with_records: "Patients covered",
      record_types: "Record types",
      recent_uploads: "Recent uploads",
    },
    groupLabels: {
      records_by_type: "Records by type",
      records_over_time: "Uploads over time",
    },
    headers: [
      { title: "Patient", key: "patient_name" },
      { title: "Title", key: "title" },
      { title: "Record type", key: "record_type" },
      { title: "File", key: "file_name" },
      { title: "Uploaded by", key: "uploaded_by" },
      { title: "Uploaded", key: "uploaded_at" },
    ],
  },
};


export default {
  props: {
    reportKey: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const report = ref(null);
    const loading = ref(true);
    const exporting = ref(false);
    const error = ref("");
    const filters = reactive({
      start_date: "",
      end_date: "",
      patient_id: "",
      staff_role: "",
      staff_name: "",
      visit_type: "",
      status: "",
    });
    const config = computed(() => configurations[props.reportKey]);
    const summaryCards = computed(() =>
      Object.entries(report.value?.summary || {}).map(([key, value]) => ({
        title: config.value.summaryLabels[key] || key,
        value,
      })),
    );
    const groups = computed(() =>
      Object.entries(report.value?.groups || {}).map(([key, items]) => ({
        title: config.value.groupLabels[key] || key,
        items,
      })),
    );
    const activeFilters = computed(() =>
      Object.fromEntries(
        Object.entries(filters).filter(
          ([key, value]) =>
            config.value.filters.includes(key) && value !== "",
        ),
      ),
    );

    function hasFilter(name) {
      return config.value.filters.includes(name);
    }

    function percentage(item, items) {
      const maximum = Math.max(...items.map((entry) => entry.count), 1);
      return Math.round((item.count / maximum) * 100);
    }

    async function loadReport() {
      loading.value = true;
      error.value = "";
      try {
        const response = await getReport(props.reportKey, activeFilters.value);
        report.value = response.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function clearFilters() {
      Object.keys(filters).forEach((key) => {
        filters[key] = "";
      });
      loadReport();
    }

    async function downloadCsv() {
      exporting.value = true;
      error.value = "";
      try {
        const blob = await exportReportCsv(
          props.reportKey,
          activeFilters.value,
        );
        const url = URL.createObjectURL(blob);
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = `${props.reportKey}.csv`;
        anchor.click();
        URL.revokeObjectURL(url);
      } catch (err) {
        error.value = err.message;
      } finally {
        exporting.value = false;
      }
    }

    watch(() => props.reportKey, loadReport);
    onMounted(loadReport);

    return {
      clearFilters,
      config,
      downloadCsv,
      error,
      exporting,
      filters,
      groups,
      hasFilter,
      loadReport,
      loading,
      percentage,
      report,
      reportKey: props.reportKey,
      summaryCards,
    };
  },
  template: `
    <div class="page-shell">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/reports" class="mb-4">
        Reports
      </v-btn>

      <PageHeader :title="config.title" :subtitle="config.subtitle" :icon="config.icon">
        <template #actions>
          <v-btn
            variant="outlined"
            prepend-icon="mdi-download-outline"
            :loading="exporting"
            @click="downloadCsv"
          >
            Export CSV
          </v-btn>
        </template>
      </PageHeader>

      <ErrorAlert :message="error" />

      <SectionCard title="Filters" icon="mdi-filter-outline" class="mb-6">
        <v-row>
          <v-col v-if="hasFilter('start_date')" cols="12" sm="6" md="3">
            <v-text-field v-model="filters.start_date" label="Start date" type="date" />
          </v-col>
          <v-col v-if="hasFilter('end_date')" cols="12" sm="6" md="3">
            <v-text-field v-model="filters.end_date" label="End date" type="date" />
          </v-col>
          <v-col v-if="hasFilter('patient_id')" cols="12" sm="6" md="3">
            <v-text-field v-model="filters.patient_id" label="Patient ID" type="number" min="1" />
          </v-col>
          <v-col v-if="hasFilter('staff_role')" cols="12" sm="6" md="3">
            <v-select v-model="filters.staff_role" label="Staff role" :items="['aide', 'nurse']" clearable />
          </v-col>
          <v-col v-if="hasFilter('staff_name')" cols="12" sm="6" md="3">
            <v-text-field v-model="filters.staff_name" label="Staff name" />
          </v-col>
          <v-col v-if="hasFilter('visit_type')" cols="12" sm="6" md="3">
            <v-text-field
              v-model="filters.visit_type"
              :label="reportKey === 'medical-records-summary' ? 'Record type' : 'Visit type'"
            />
          </v-col>
          <v-col v-if="hasFilter('status')" cols="12" sm="6" md="3">
            <v-select v-model="filters.status" label="Status" :items="config.statuses" clearable />
          </v-col>
        </v-row>
        <div class="d-flex flex-wrap justify-end ga-3">
          <v-btn variant="text" @click="clearFilters">Clear filters</v-btn>
          <v-btn color="primary" prepend-icon="mdi-filter-check-outline" :loading="loading" @click="loadReport">
            Apply filters
          </v-btn>
        </div>
      </SectionCard>

      <LoadingState v-if="loading" type="heading, card, card, table" />

      <template v-else-if="report">
        <v-row class="mb-6">
          <v-col v-for="card in summaryCards" :key="card.title" cols="12" sm="6" lg="3">
            <v-card class="metric-card metric-card--primary">
              <v-card-text class="pa-5">
                <div class="metric-card__value">{{ card.value }}</div>
                <div class="metric-card__title">{{ card.title }}</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <EmptyState
          v-if="!report.rows.length"
          icon="mdi-chart-box-outline"
          title="No report data"
          description="No records match the selected filters."
          class="mb-6"
        />

        <v-row v-if="report.rows.length" class="mb-6">
          <v-col v-for="group in groups" :key="group.title" cols="12" md="6">
            <SectionCard :title="group.title" icon="mdi-chart-bar">
              <div v-if="!group.items.length" class="text-medium-emphasis">No grouped data available.</div>
              <div v-for="item in group.items.slice(0, 12)" :key="item.label" class="chart-row">
                <div class="chart-row__label">
                  <span>{{ item.label }}</span>
                  <strong>{{ item.count }}</strong>
                </div>
                <v-progress-linear
                  :model-value="percentage(item, group.items)"
                  color="primary"
                  height="8"
                  rounded
                />
              </div>
            </SectionCard>
          </v-col>
        </v-row>

        <SectionCard title="Report details" icon="mdi-table" class="data-card">
          <v-data-table
            :headers="config.headers"
            :items="report.rows"
            density="comfortable"
            :items-per-page="15"
          >
            <template #no-data>
              <EmptyState
                icon="mdi-table-off"
                title="No rows to display"
                description="Adjust the filters and try again."
              />
            </template>
            <template #[\`item.status\`]="{ item }">
              <StatusChip :status="item.status" />
            </template>
          </v-data-table>
        </SectionCard>
      </template>
    </div>
  `,
};
