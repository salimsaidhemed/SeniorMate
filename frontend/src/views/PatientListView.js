import { computed, onMounted, ref } from "vue";

import { deletePatient, listPatients } from "../services/patients.js";

export default {
  setup() {
    const patients = ref([]);
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const deleting = ref(false);
    const selectedPatient = ref(null);
    const confirmDelete = ref(false);

    const headers = [
      { title: "Full name", key: "full_name" },
      { title: "Date of birth", key: "date_of_birth" },
      { title: "Gender", key: "gender" },
      { title: "Phone", key: "phone" },
      { title: "Status", key: "status" },
      { title: "Actions", key: "actions", sortable: false },
    ];

    const rows = computed(() =>
      patients.value.map((patient) => ({
        ...patient,
        full_name: `${patient.first_name} ${patient.last_name}`,
      }))
    );

    async function loadPatients() {
      loading.value = true;
      error.value = "";

      try {
        const response = await listPatients();
        patients.value = response.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function askDelete(patient) {
      selectedPatient.value = patient;
      confirmDelete.value = true;
    }

    async function removePatient() {
      if (!selectedPatient.value) return;

      deleting.value = true;
      error.value = "";
      success.value = "";

      try {
        await deletePatient(selectedPatient.value.id);
        success.value = "Patient deleted successfully.";
        confirmDelete.value = false;
        selectedPatient.value = null;
        await loadPatients();
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    onMounted(loadPatients);

    return {
      askDelete,
      confirmDelete,
      deleting,
      error,
      headers,
      loadPatients,
      loading,
      patients,
      removePatient,
      rows,
      selectedPatient,
      success,
    };
  },
  template: `
    <div class="page-shell">
      <PageHeader
        title="Patients"
        subtitle="Manage patient demographics and emergency contacts."
        icon="mdi-account-heart-outline"
      >
        <template #actions>
          <v-btn color="primary" prepend-icon="mdi-plus" to="/patients/new">
            New patient
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
              icon="mdi-account-plus-outline"
              title="No patients yet"
              description="Create the first patient profile to begin tracking care."
              action-label="Create patient"
              action-to="/patients/new"
            />
          </template>

          <template #[\`item.status\`]="{ item }">
            <StatusChip :status="item.status" />
          </template>

          <template #[\`item.actions\`]="{ item }">
            <div class="table-actions">
              <v-btn icon="mdi-eye-outline" variant="text" :to="\`/patients/\${item.id}\`" aria-label="View patient" />
              <v-btn icon="mdi-pencil-outline" variant="text" :to="\`/patients/\${item.id}/edit\`" aria-label="Edit patient" />
              <v-btn icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete patient" @click="askDelete(item)" />
            </div>
          </template>
        </v-data-table>
      </v-card>

      <ConfirmDialog
        v-model="confirmDelete"
        title="Delete patient"
        :message="\`Delete \${selectedPatient?.full_name || 'this patient'}? This cannot be undone.\`"
        :loading="deleting"
        @confirm="removePatient"
      />
    </div>
  `,
};
