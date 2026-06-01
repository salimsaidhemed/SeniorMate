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
    const filters = ref({
      search: "",
      status: "",
      gender: "",
      page: 1,
      per_page: 10,
    });
    const pagination = ref({ page: 1, per_page: 10, total: 0, pages: 0 });

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
        const response = await listPatients(filters.value);
        patients.value = response.data;
        pagination.value = response.pagination || pagination.value;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    async function applyFilters() {
      filters.value.page = 1;
      await loadPatients();
    }

    async function clearFilters() {
      filters.value = {
        search: "",
        status: "",
        gender: "",
        page: 1,
        per_page: 10,
      };
      await loadPatients();
    }

    async function changePage(page) {
      filters.value.page = page;
      await loadPatients();
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
      applyFilters,
      changePage,
      clearFilters,
      confirmDelete,
      deleting,
      error,
      filters,
      headers,
      loadPatients,
      loading,
      pagination,
      patients,
      removePatient,
      rows,
      selectedPatient,
      success,
    };
  },
  template: `
    <v-container class="py-8" style="max-width: 1280px;">
      <v-row align="center" class="mb-5">
        <v-col cols="12" md="8">
          <h1 class="text-h4 font-weight-bold mb-1">Patients</h1>
          <p class="text-body-2 text-medium-emphasis mb-0">Manage patient demographics and emergency contacts.</p>
        </v-col>
        <v-col cols="12" md="4" class="text-md-right">
          <v-btn color="primary" prepend-icon="mdi-plus" to="/patients/new">
            New patient
          </v-btn>
        </v-col>
      </v-row>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>
      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        {{ success }}
      </v-alert>

      <v-card class="mb-4">
        <v-card-text>
          <v-row align="center">
            <v-col cols="12" md="5">
              <v-text-field
                v-model="filters.search"
                label="Search patients"
                prepend-inner-icon="mdi-magnify"
                clearable
                hide-details
                @keyup.enter="applyFilters"
              />
            </v-col>
            <v-col cols="12" md="2">
              <v-select
                v-model="filters.status"
                label="Status"
                :items="['active', 'inactive']"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="2">
              <v-select
                v-model="filters.gender"
                label="Gender"
                :items="['female', 'male', 'nonbinary', 'other']"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3" class="d-flex ga-2 justify-md-end">
              <v-btn color="primary" :loading="loading" @click="applyFilters">Apply</v-btn>
              <v-btn variant="text" @click="clearFilters">Clear</v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

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
              <v-icon icon="mdi-account-heart-outline" size="40" class="mb-3" />
              <div class="text-h6 mb-2">No patients yet</div>
              <v-btn color="primary" variant="flat" to="/patients/new">Create patient</v-btn>
            </div>
          </template>

          <template #[\`item.status\`]="{ item }">
            <v-chip :color="item.status === 'active' ? 'success' : 'grey'" size="small">
              {{ item.status }}
            </v-chip>
          </template>

          <template #[\`item.actions\`]="{ item }">
            <v-btn icon="mdi-eye-outline" variant="text" :to="\`/patients/\${item.id}\`" aria-label="View patient" />
            <v-btn icon="mdi-pencil-outline" variant="text" :to="\`/patients/\${item.id}/edit\`" aria-label="Edit patient" />
            <v-btn icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete patient" @click="askDelete(item)" />
          </template>
        </v-data-table>
      </v-card>

      <div class="d-flex justify-end mt-4" v-if="pagination.pages > 1">
        <v-pagination
          :model-value="pagination.page"
          :length="pagination.pages"
          total-visible="5"
          @update:model-value="changePage"
        />
      </div>

      <v-dialog v-model="confirmDelete" max-width="440">
        <v-card>
          <v-card-title>Delete patient</v-card-title>
          <v-card-text>
            Delete {{ selectedPatient?.full_name }}?
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="confirmDelete = false">Cancel</v-btn>
            <v-btn color="error" variant="flat" :loading="deleting" @click="removePatient">
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  `,
};
