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
    <v-container class="py-8" style="max-width: 1440px;">
      <v-row align="center" class="mb-5">
        <v-col cols="12" md="8">
          <h1 class="text-h4 font-weight-bold mb-1">Visits</h1>
          <p class="text-body-2 text-medium-emphasis mb-0">Track caregiver and nursing visits for active patients.</p>
        </v-col>
        <v-col cols="12" md="4" class="text-md-right">
          <v-btn color="primary" prepend-icon="mdi-plus" to="/visits/new">
            New visit
          </v-btn>
        </v-col>
      </v-row>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>
      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        {{ success }}
      </v-alert>

      <v-card>
        <v-data-table
          :headers="headers"
          :items="rows"
          :loading="loading"
          item-value="id"
        >
          <template #loading>
            <v-skeleton-loader type="table-row@5" />
          </template>

          <template #no-data>
            <div class="pa-8 text-center">
              <v-icon icon="mdi-calendar-clock-outline" size="40" class="mb-3" />
              <div class="text-h6 mb-2">No visits yet</div>
              <v-btn color="primary" variant="flat" to="/visits/new">Create visit</v-btn>
            </div>
          </template>

          <template #[\`item.patient_name\`]="{ item }">
            <router-link :to="\`/patients/\${item.patient_id}\`">{{ item.patient_name }}</router-link>
          </template>

          <template #[\`item.status\`]="{ item }">
            <v-chip :color="item.status === 'completed' ? 'success' : item.status === 'cancelled' ? 'grey' : 'primary'" size="small">
              {{ item.status }}
            </v-chip>
          </template>

          <template #[\`item.actions\`]="{ item }">
            <v-btn icon="mdi-eye-outline" variant="text" :to="\`/visits/\${item.id}\`" aria-label="View visit" />
            <v-btn icon="mdi-pencil-outline" variant="text" :to="\`/visits/\${item.id}/edit\`" aria-label="Edit visit" />
            <v-btn icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete visit" @click="askDelete(item)" />
          </template>
        </v-data-table>
      </v-card>

      <v-dialog v-model="confirmDelete" max-width="440">
        <v-card>
          <v-card-title>Delete visit</v-card-title>
          <v-card-text>
            Delete {{ selectedVisit?.visit_type }} for {{ selectedVisit?.patient_name }}?
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="confirmDelete = false">Cancel</v-btn>
            <v-btn color="error" variant="flat" :loading="deleting" @click="removeVisit">
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  `,
};
