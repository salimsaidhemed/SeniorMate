import { computed, onMounted, ref } from "vue";

import { getDashboardStats } from "../services/dashboard.js";

export default {
  setup() {
    const stats = ref(null);
    const loading = ref(true);
    const error = ref("");

    const cards = computed(() => [
      {
        title: "Total Patients",
        value: stats.value?.total_patients ?? 0,
        icon: "mdi-account-heart-outline",
        color: "primary",
      },
      {
        title: "Active Patients",
        value: stats.value?.active_patients ?? 0,
        icon: "mdi-account-check-outline",
        color: "success",
      },
      {
        title: "Visits This Month",
        value: stats.value?.visits_this_month ?? 0,
        icon: "mdi-calendar-clock-outline",
        color: "secondary",
      },
      {
        title: "Aide Notes This Month",
        value: stats.value?.aide_notes_this_month ?? 0,
        icon: "mdi-clipboard-check-outline",
        color: "teal",
      },
      {
        title: "Nurse Notes This Month",
        value: stats.value?.nurse_notes_this_month ?? 0,
        icon: "mdi-clipboard-pulse-outline",
        color: "indigo",
      },
    ]);
    const chartSections = computed(() => [
      {
        title: "Patients by Status",
        items: stats.value?.patients_by_status || [],
        color: "primary",
      },
      {
        title: "Patients by Gender",
        items: stats.value?.patients_by_gender || [],
        color: "success",
      },
      {
        title: "Visits by Type",
        items: stats.value?.visits_by_type || [],
        color: "secondary",
      },
      {
        title: "Visits by Status",
        items: stats.value?.visits_by_status || [],
        color: "teal",
      },
    ]);
    const recentVisitHeaders = [
      { title: "Patient", key: "patient_name" },
      { title: "Visit date", key: "visit_date" },
      { title: "Visit type", key: "visit_type" },
      { title: "Staff role", key: "staff_role" },
      { title: "Status", key: "status" },
      { title: "Actions", key: "actions", sortable: false },
    ];
    const hasDashboardData = computed(() =>
      Boolean(
        stats.value &&
          (stats.value.total_patients ||
            stats.value.total_visits ||
            stats.value.aide_notes_this_month ||
            stats.value.nurse_notes_this_month)
      )
    );

    function chartMax(items) {
      return Math.max(...items.map((item) => item.count), 1);
    }

    function percentage(item, items) {
      return Math.round((item.count / chartMax(items)) * 100);
    }

    async function loadDashboard() {
      loading.value = true;
      error.value = "";

      try {
        const response = await getDashboardStats();
        stats.value = response.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadDashboard);

    return {
      cards,
      chartSections,
      error,
      hasDashboardData,
      percentage,
      loading,
      loadDashboard,
      recentVisitHeaders,
      stats,
    };
  },
  template: `
    <v-container class="py-8" style="max-width: 1280px;">
      <v-row align="center" class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h4 font-weight-bold mb-2">Care operations dashboard</h1>
          <p class="text-body-1 text-medium-emphasis mb-0">
            A quick view of patient, visit, and care-note activity.
          </p>
        </v-col>
        <v-col cols="12" md="4" class="text-md-right">
          <v-btn color="primary" variant="flat" :loading="loading" @click="loadDashboard">
            Refresh dashboard
          </v-btn>
        </v-col>
      </v-row>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-6">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, card, card, table" />

      <template v-else-if="stats">
        <v-alert v-if="!hasDashboardData" type="info" variant="tonal" class="mb-6">
          No patient, visit, or care-note activity has been recorded yet.
        </v-alert>

        <v-row class="mb-6">
          <v-col v-for="card in cards" :key="card.title" cols="12" sm="6" lg="2">
            <v-card>
              <v-card-text>
                <div class="d-flex align-center justify-space-between mb-4">
                  <v-icon :icon="card.icon" :color="card.color" size="32" />
                  <div class="text-h4 font-weight-bold">{{ card.value }}</div>
                </div>
                <div class="text-body-2 text-medium-emphasis">{{ card.title }}</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row class="mb-6">
          <v-col v-for="section in chartSections" :key="section.title" cols="12" md="6">
            <v-card class="h-100">
              <v-card-title>{{ section.title }}</v-card-title>
              <v-card-text>
                <div v-if="!section.items.length" class="text-medium-emphasis">
                  No data available.
                </div>
                <div v-for="item in section.items" :key="item.label" class="mb-4">
                  <div class="d-flex justify-space-between mb-1">
                    <span>{{ item.label }}</span>
                    <strong>{{ item.count }}</strong>
                  </div>
                  <v-progress-linear
                    :model-value="percentage(item, section.items)"
                    :color="section.color"
                    height="10"
                    rounded
                  />
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card>
          <v-card-title>Recent Visits</v-card-title>
          <v-data-table
            :headers="recentVisitHeaders"
            :items="stats.recent_visits"
            item-value="id"
          >
            <template #no-data>
              <div class="pa-8 text-center">
                <v-icon icon="mdi-calendar-clock-outline" size="40" class="mb-3" />
                <div class="text-h6 mb-2">No recent visits</div>
              </div>
            </template>

            <template #[\`item.patient_name\`]="{ item }">
              {{ item.patient_name || 'Patient not available' }}
            </template>

            <template #[\`item.status\`]="{ item }">
              <v-chip :color="item.status === 'completed' ? 'success' : item.status === 'cancelled' ? 'grey' : 'primary'" size="small">
                {{ item.status }}
              </v-chip>
            </template>

            <template #[\`item.actions\`]="{ item }">
              <v-btn icon="mdi-eye-outline" variant="text" :to="\`/visits/\${item.id}\`" aria-label="View visit" />
            </template>
          </v-data-table>
        </v-card>
      </template>
    </v-container>
  `,
};
