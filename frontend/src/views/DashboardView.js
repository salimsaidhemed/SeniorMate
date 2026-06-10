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
        caption: `${stats.value?.inactive_patients ?? 0} inactive`,
      },
      {
        title: "Active Patients",
        value: stats.value?.active_patients ?? 0,
        icon: "mdi-account-check-outline",
        color: "success",
        caption: "Currently receiving care",
      },
      {
        title: "Visits This Month",
        value: stats.value?.visits_this_month ?? 0,
        icon: "mdi-calendar-clock-outline",
        color: "secondary",
        caption: `${stats.value?.total_visits ?? 0} visits overall`,
      },
      {
        title: "Aide Notes This Month",
        value: stats.value?.aide_notes_this_month ?? 0,
        icon: "mdi-clipboard-check-outline",
        color: "teal",
        caption: "Home health aide records",
      },
      {
        title: "Nurse Notes This Month",
        value: stats.value?.nurse_notes_this_month ?? 0,
        icon: "mdi-clipboard-pulse-outline",
        color: "indigo",
        caption: "Clinical progress records",
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
    <div class="page-shell">
      <PageHeader
        title="Care operations dashboard"
        subtitle="A quick view of patient, visit, and care-note activity."
        icon="mdi-view-dashboard-outline"
      >
        <template #actions>
          <v-btn color="primary" variant="flat" :loading="loading" @click="loadDashboard">
            Refresh dashboard
          </v-btn>
        </template>
      </PageHeader>

      <ErrorAlert :message="error" />

      <LoadingState v-if="loading" type="heading, card, card, table" />

      <template v-else-if="stats">
        <EmptyState
          v-if="!hasDashboardData"
          icon="mdi-chart-box-outline"
          title="No activity yet"
          description="Patient, visit, and care-note activity will appear here as records are added."
          class="mb-6"
        />

        <v-row class="dashboard-metrics mb-7">
          <v-col v-for="card in cards" :key="card.title" cols="12" sm="6" lg>
            <v-card class="metric-card" :class="\`metric-card--\${card.color}\`">
              <v-card-text class="pa-5">
                <div class="metric-card__topline">
                  <div class="metric-card__icon">
                    <v-icon :icon="card.icon" :color="card.color" size="24" />
                  </div>
                  <div class="metric-card__value">{{ card.value }}</div>
                </div>
                <div class="metric-card__title">{{ card.title }}</div>
                <div class="metric-card__caption">{{ card.caption }}</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row class="mb-7">
          <v-col v-for="section in chartSections" :key="section.title" cols="12" md="6">
            <SectionCard :title="section.title" icon="mdi-chart-bar">
                <div v-if="!section.items.length" class="text-medium-emphasis">
                  No data available.
                </div>
                <div v-for="item in section.items" :key="item.label" class="chart-row">
                  <div class="chart-row__label">
                    <span>{{ item.label }}</span>
                    <strong>{{ item.count }}</strong>
                  </div>
                  <v-progress-linear
                    :model-value="percentage(item, section.items)"
                    :color="section.color"
                    height="8"
                    rounded
                  />
                </div>
            </SectionCard>
          </v-col>
        </v-row>

        <SectionCard
          title="Recent Visits"
          subtitle="The latest care activity across patients."
          icon="mdi-calendar-clock-outline"
          class="data-card"
        >
            <v-data-table
              :headers="recentVisitHeaders"
              :items="stats.recent_visits"
              item-value="id"
              density="comfortable"
            >
              <template #no-data>
                <EmptyState
                  icon="mdi-calendar-blank-outline"
                  title="No recent visits"
                  description="New visits will appear here."
                />
              </template>

              <template #[\`item.patient_name\`]="{ item }">
                {{ item.patient_name || 'Patient not available' }}
              </template>

              <template #[\`item.status\`]="{ item }">
                <StatusChip :status="item.status" />
              </template>

              <template #[\`item.actions\`]="{ item }">
                <div class="table-actions">
                  <v-btn
                    icon="mdi-arrow-right"
                    variant="text"
                    :to="\`/visits/\${item.id}\`"
                    aria-label="Open visit"
                    title="Open visit"
                  />
                </div>
              </template>
            </v-data-table>
        </SectionCard>
      </template>
    </div>
  `,
};
