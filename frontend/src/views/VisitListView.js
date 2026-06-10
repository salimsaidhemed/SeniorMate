import { computed, onMounted, ref } from "vue";

import { listPatients } from "../services/patients.js";
import { deleteVisit, listVisits } from "../services/visits.js";

export default {
  setup() {
    const visits = ref([]);
    const patients = ref([]);
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const deleting = ref(false);
    const selectedVisit = ref(null);
    const confirmDelete = ref(false);

    const headers = [
      { title: "Patient", key: "patient_name" },
      { title: "Visit date", key: "visit_date" },
      { title: "Visit type", key: "visit_type" },
      { title: "Staff name", key: "staff_name" },
      { title: "Staff role", key: "staff_role" },
      { title: "Time in", key: "time_in" },
      { title: "Time out", key: "time_out" },
      { title: "Status", key: "status" },
      { title: "Actions", key: "actions", sortable: false },
    ];

    const patientNames = computed(() =>
      Object.fromEntries(
        patients.value.map((patient) => [
          patient.id,
          `${patient.first_name} ${patient.last_name}`,
        ])
      )
    );

    const rows = computed(() =>
      visits.value.map((visit) => ({
        ...visit,
        patient_name: patientNames.value[visit.patient_id] || `Patient #${visit.patient_id}`,
      }))
    );

    async function loadVisits() {
      loading.value = true;
      error.value = "";

      try {
        const [visitResponse, patientResponse] = await Promise.all([
          listVisits(),
          listPatients(),
        ]);
        visits.value = visitResponse.data;
        patients.value = patientResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function askDelete(visit) {
      selectedVisit.value = visit;
      confirmDelete.value = true;
    }

    async function removeVisit() {
      if (!selectedVisit.value) return;

      deleting.value = true;
      error.value = "";
      success.value = "";

      try {
        await deleteVisit(selectedVisit.value.id);
        success.value = "Visit deleted successfully.";
        confirmDelete.value = false;
        selectedVisit.value = null;
        await loadVisits();
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    onMounted(loadVisits);

    return {
      askDelete,
      confirmDelete,
      deleting,
      error,
      headers,
      loading,
      removeVisit,
      rows,
      selectedVisit,
      success,
    };
  },
  template: `
    <div class="page-shell">
      <PageHeader
        title="Visits"
        subtitle="Track caregiver and nursing visits for active patients."
        icon="mdi-calendar-clock-outline"
      >
        <template #actions>
          <v-btn color="primary" prepend-icon="mdi-plus" to="/visits/new">
            New visit
          </v-btn>
        </template>
      </PageHeader>

      <ErrorAlert :message="error" />
      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        {{ success }}
      </v-alert>

      <v-card class="data-card">
        <v-data-table
          :headers="headers"
          :items="rows"
          :loading="loading"
          item-value="id"
        >
          <template #loading>
            <LoadingState />
          </template>

          <template #no-data>
            <EmptyState
              icon="mdi-calendar-plus-outline"
              title="No visits yet"
              description="Schedule the first patient visit to begin tracking care activity."
              action-label="Create visit"
              action-to="/visits/new"
            />
          </template>

          <template #[\`item.patient_name\`]="{ item }">
            <router-link :to="\`/patients/\${item.patient_id}\`">{{ item.patient_name }}</router-link>
          </template>

          <template #[\`item.status\`]="{ item }">
            <StatusChip :status="item.status" />
          </template>

          <template #[\`item.actions\`]="{ item }">
            <div class="table-actions">
              <v-btn icon="mdi-eye-outline" variant="text" :to="\`/visits/\${item.id}\`" aria-label="View visit" title="View visit" />
              <v-btn icon="mdi-pencil-outline" variant="text" :to="\`/visits/\${item.id}/edit\`" aria-label="Edit visit" title="Edit visit" />
              <v-btn icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete visit" title="Delete visit" @click="askDelete(item)" />
            </div>
          </template>
        </v-data-table>
      </v-card>

      <ConfirmDialog
        v-model="confirmDelete"
        title="Delete visit"
        :message="\`Delete \${selectedVisit?.visit_type || 'this visit'} for \${selectedVisit?.patient_name || 'this patient'}?\`"
        :loading="deleting"
        @confirm="removeVisit"
      />
    </div>
  `,
};
