import { computed, onMounted, ref } from "vue";

import { deleteAideNote, listAideNotes } from "../services/aideNotes.js";
import { canCreateAideNote } from "../permissions.js";
import { listPatients } from "../services/patients.js";
import { listVisits } from "../services/visits.js";

export default {
  setup() {
    const aideNotes = ref([]);
    const patients = ref([]);
    const visits = ref([]);
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const deleting = ref(false);
    const selectedNote = ref(null);
    const confirmDelete = ref(false);
    const filters = ref({
      patient_id: "",
      visit_id: "",
      aide_name: "",
      start_date: "",
      end_date: "",
      page: 1,
      per_page: 10,
    });
    const pagination = ref({ page: 1, per_page: 10, total: 0, pages: 0 });

    const headers = [
      { title: "Patient", key: "patient_name" },
      { title: "Visit date", key: "visit_date" },
      { title: "Aide name", key: "aide_name" },
      { title: "Time in", key: "time_in" },
      { title: "Time out", key: "time_out" },
      { title: "Signature date", key: "signature_date" },
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
    const patientOptions = computed(() =>
      patients.value.map((patient) => ({
        title: `${patient.first_name} ${patient.last_name}`,
        value: patient.id,
      }))
    );
    const visitDates = computed(() =>
      Object.fromEntries(visits.value.map((visit) => [visit.id, visit.visit_date]))
    );
    const rows = computed(() =>
      aideNotes.value.map((note) => ({
        ...note,
        patient_name: patientNames.value[note.patient_id] || `Patient #${note.patient_id}`,
        visit_date: visitDates.value[note.visit_id] || "Not available",
      }))
    );

    async function loadAideNotes() {
      loading.value = true;
      error.value = "";

      try {
        const [noteResponse, patientResponse, visitResponse] = await Promise.all([
          listAideNotes(filters.value),
          listPatients({ per_page: 100 }),
          listVisits({ per_page: 100 }),
        ]);
        aideNotes.value = noteResponse.data;
        pagination.value = noteResponse.pagination || pagination.value;
        patients.value = patientResponse.data;
        visits.value = visitResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    async function applyFilters() {
      filters.value.page = 1;
      await loadAideNotes();
    }

    async function clearFilters() {
      filters.value = {
        patient_id: "",
        visit_id: "",
        aide_name: "",
        start_date: "",
        end_date: "",
        page: 1,
        per_page: 10,
      };
      await loadAideNotes();
    }

    async function changePage(page) {
      filters.value.page = page;
      await loadAideNotes();
    }

    function askDelete(note) {
      selectedNote.value = note;
      confirmDelete.value = true;
    }

    async function removeAideNote() {
      if (!selectedNote.value) return;

      deleting.value = true;
      error.value = "";
      success.value = "";

      try {
        await deleteAideNote(selectedNote.value.id);
        success.value = "Aide note deleted successfully.";
        confirmDelete.value = false;
        selectedNote.value = null;
        await loadAideNotes();
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    onMounted(loadAideNotes);

    return {
      askDelete,
      applyFilters,
      changePage,
      clearFilters,
      confirmDelete,
      canCreateAideNote,
      deleting,
      error,
      filters,
      headers,
      loading,
      pagination,
      patientOptions,
      removeAideNote,
      rows,
      selectedNote,
      success,
    };
  },
  template: `
    <div class="page-shell">
      <PageHeader
        title="Aide Notes"
        subtitle="Review Home Health Aide documentation linked to visits."
        icon="mdi-clipboard-check-outline"
      />

      <ErrorAlert :message="error" />
      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        {{ success }}
      </v-alert>

      <v-card class="mb-4">
        <v-card-text>
          <v-row align="center">
            <v-col cols="12" md="3">
              <v-text-field v-model="filters.aide_name" label="Aide name" prepend-inner-icon="mdi-magnify" clearable hide-details @keyup.enter="applyFilters" />
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="filters.patient_id"
                label="Patient"
                :items="patientOptions"
                item-title="title"
                item-value="value"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="2">
              <v-text-field v-model="filters.start_date" label="Start date" type="date" hide-details />
            </v-col>
            <v-col cols="12" md="2">
              <v-text-field v-model="filters.end_date" label="End date" type="date" hide-details />
            </v-col>
            <v-col cols="12" md="2" class="d-flex ga-2 justify-md-end">
              <v-btn color="primary" :loading="loading" @click="applyFilters">Apply</v-btn>
              <v-btn variant="text" @click="clearFilters">Clear</v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <v-card class="data-card">
        <v-data-table :headers="headers" :items="rows" :loading="loading" item-value="id">
          <template #loading>
            <LoadingState />
          </template>

          <template #no-data>
            <EmptyState
              icon="mdi-clipboard-text-outline"
              title="No aide notes yet"
              description="Aide notes created from visit details will appear here."
            />
          </template>

          <template #[\`item.patient_name\`]="{ item }">
            <router-link :to="\`/patients/\${item.patient_id}\`">{{ item.patient_name }}</router-link>
          </template>

          <template #[\`item.actions\`]="{ item }">
            <div class="table-actions">
              <v-btn icon="mdi-eye-outline" variant="text" :to="\`/aide-notes/\${item.id}\`" aria-label="View aide note" title="View aide note" />
              <v-btn v-if="canCreateAideNote()" icon="mdi-pencil-outline" variant="text" :to="\`/aide-notes/\${item.id}/edit\`" aria-label="Edit aide note" title="Edit aide note" />
              <v-btn v-if="canCreateAideNote()" icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete aide note" title="Delete aide note" @click="askDelete(item)" />
            </div>
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

      <ConfirmDialog
        v-model="confirmDelete"
        title="Delete aide note"
        :message="\`Delete the aide note for \${selectedNote?.patient_name || 'this patient'}?\`"
        :loading="deleting"
        @confirm="removeAideNote"
      />
    </div>
  `,
};
