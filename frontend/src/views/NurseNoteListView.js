import { computed, onMounted, ref } from "vue";

import { deleteNurseNote, listNurseNotes } from "../services/nurseNotes.js";
import { listPatients } from "../services/patients.js";
import { listVisits } from "../services/visits.js";

export default {
  setup() {
    const nurseNotes = ref([]);
    const patients = ref([]);
    const visits = ref([]);
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const deleting = ref(false);
    const selectedNote = ref(null);
    const confirmDelete = ref(false);

    const headers = [
      { title: "Patient", key: "patient_name" },
      { title: "Visit date", key: "visit_date" },
      { title: "Diagnosis", key: "diagnosis" },
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
    const visitDates = computed(() =>
      Object.fromEntries(visits.value.map((visit) => [visit.id, visit.visit_date]))
    );
    const rows = computed(() =>
      nurseNotes.value.map((note) => ({
        ...note,
        patient_name: patientNames.value[note.patient_id] || `Patient #${note.patient_id}`,
        visit_date: visitDates.value[note.visit_id] || "Not available",
      }))
    );

    async function loadNurseNotes() {
      loading.value = true;
      error.value = "";

      try {
        const [noteResponse, patientResponse, visitResponse] = await Promise.all([
          listNurseNotes(),
          listPatients(),
          listVisits(),
        ]);
        nurseNotes.value = noteResponse.data;
        patients.value = patientResponse.data;
        visits.value = visitResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function askDelete(note) {
      selectedNote.value = note;
      confirmDelete.value = true;
    }

    async function removeNurseNote() {
      if (!selectedNote.value) return;

      deleting.value = true;
      error.value = "";
      success.value = "";

      try {
        await deleteNurseNote(selectedNote.value.id);
        success.value = "Nurse note deleted successfully.";
        confirmDelete.value = false;
        selectedNote.value = null;
        await loadNurseNotes();
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    onMounted(loadNurseNotes);

    return {
      askDelete,
      confirmDelete,
      deleting,
      error,
      headers,
      loading,
      removeNurseNote,
      rows,
      selectedNote,
      success,
    };
  },
  template: `
    <div class="page-shell">
      <PageHeader
        title="Nurse Notes"
        subtitle="Review Nurses Progress Notes linked to clinical visits."
        icon="mdi-clipboard-pulse-outline"
      />

      <ErrorAlert :message="error" />
      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        {{ success }}
      </v-alert>

      <v-card class="data-card">
        <v-data-table :headers="headers" :items="rows" :loading="loading" item-value="id">
          <template #loading>
            <LoadingState />
          </template>

          <template #no-data>
            <EmptyState
              icon="mdi-clipboard-text-outline"
              title="No nurse notes yet"
              description="Nurse notes created from visit details will appear here."
            />
          </template>

          <template #[\`item.patient_name\`]="{ item }">
            <router-link :to="\`/patients/\${item.patient_id}\`">{{ item.patient_name }}</router-link>
          </template>

          <template #[\`item.actions\`]="{ item }">
            <div class="table-actions">
              <v-btn icon="mdi-eye-outline" variant="text" :to="\`/nurse-notes/\${item.id}\`" aria-label="View nurse note" title="View nurse note" />
              <v-btn icon="mdi-pencil-outline" variant="text" :to="\`/nurse-notes/\${item.id}/edit\`" aria-label="Edit nurse note" title="Edit nurse note" />
              <v-btn icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete nurse note" title="Delete nurse note" @click="askDelete(item)" />
            </div>
          </template>
        </v-data-table>
      </v-card>

      <ConfirmDialog
        v-model="confirmDelete"
        title="Delete nurse note"
        :message="\`Delete the nurse note for \${selectedNote?.patient_name || 'this patient'}?\`"
        :loading="deleting"
        @confirm="removeNurseNote"
      />
    </div>
  `,
};
