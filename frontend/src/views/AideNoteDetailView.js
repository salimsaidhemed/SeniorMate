import { computed, onMounted, ref } from "vue";

import { getAideNote } from "../services/aideNotes.js";
import { listPatients } from "../services/patients.js";
import { listVisits } from "../services/visits.js";

const sectionLabels = {
  personal_care: "Personal Care",
  nutrition: "Nutrition",
  mental_status: "Mental Status",
  elimination: "Elimination",
  activity: "Activity",
  assistive_devices: "Assistive Devices",
  housekeeping: "Housekeeping",
};

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const aideNote = ref(null);
    const patients = ref([]);
    const visits = ref([]);
    const loading = ref(true);
    const error = ref("");

    const patient = computed(() =>
      patients.value.find((candidate) => candidate.id === aideNote.value?.patient_id)
    );
    const visit = computed(() =>
      visits.value.find((candidate) => candidate.id === aideNote.value?.visit_id)
    );
    const patientName = computed(() =>
      patient.value
        ? `${patient.value.first_name} ${patient.value.last_name}`
        : aideNote.value
          ? `Patient #${aideNote.value.patient_id}`
          : ""
    );
    const checklistSections = computed(() =>
      Object.entries(sectionLabels).map(([key, title]) => ({
        key,
        title,
        items: aideNote.value?.[key]?.completed || [],
        detail: aideNote.value?.[key],
      }))
    );

    function formatChecklist(section) {
      if (!section.detail) return "Not documented";
      if (section.items.length) return section.items.join(", ");

      return JSON.stringify(section.detail);
    }

    async function loadAideNote() {
      loading.value = true;
      error.value = "";

      try {
        const [noteResponse, patientResponse, visitResponse] = await Promise.all([
          getAideNote(props.id),
          listPatients(),
          listVisits(),
        ]);
        aideNote.value = noteResponse.data;
        patients.value = patientResponse.data;
        visits.value = visitResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadAideNote);

    return {
      aideNote,
      checklistSections,
      error,
      formatChecklist,
      loading,
      patientName,
      visit,
    };
  },
  template: `
    <v-container class="py-8" style="max-width: 1120px;">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/aide-notes" class="mb-4">
        Aide Notes
      </v-btn>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <template v-else-if="aideNote">
        <v-row align="center" class="mb-5">
          <v-col cols="12" md="8">
            <h1 class="text-h4 font-weight-bold mb-2">Aide Note</h1>
            <div class="text-body-1 text-medium-emphasis">
              {{ patientName }} · {{ visit?.visit_date || 'Visit date not available' }}
            </div>
          </v-col>
          <v-col cols="12" md="4" class="text-md-right">
            <v-btn color="primary" prepend-icon="mdi-pencil-outline" :to="\`/aide-notes/\${aideNote.id}/edit\`">
              Edit aide note
            </v-btn>
          </v-col>
        </v-row>

        <v-row class="mb-5">
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Visit and staff</v-card-title>
              <v-list>
                <v-list-item title="Patient" :subtitle="patientName" :to="\`/patients/\${aideNote.patient_id}\`" />
                <v-list-item title="Visit" :subtitle="visit?.visit_type || 'Not available'" :to="\`/visits/\${aideNote.visit_id}\`" />
                <v-list-item title="Aide name" :subtitle="aideNote.aide_name || 'Not provided'" />
                <v-list-item title="Time in" :subtitle="aideNote.time_in || 'Not provided'" />
                <v-list-item title="Time out" :subtitle="aideNote.time_out || 'Not provided'" />
                <v-list-item title="Signature date" :subtitle="aideNote.signature_date || 'Not provided'" />
              </v-list>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Additional Notes</v-card-title>
              <v-card-text>{{ aideNote.additional_notes || 'Not provided' }}</v-card-text>
              <v-divider />
              <v-card-title>Signature Data</v-card-title>
              <v-card-text>{{ aideNote.signature_data || 'Not provided' }}</v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="section in checklistSections" :key="section.key" cols="12" md="6">
            <v-card>
              <v-card-title>{{ section.title }}</v-card-title>
              <v-card-text>{{ formatChecklist(section) }}</v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  `,
};
