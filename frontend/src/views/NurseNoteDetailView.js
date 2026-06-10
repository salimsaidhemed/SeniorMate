import { computed, onMounted, ref } from "vue";

import { getNurseNote } from "../services/nurseNotes.js";
import { listPatients } from "../services/patients.js";
import { listVisits } from "../services/visits.js";

const clinicalSectionLabels = {
  living_arrangements: "Patient / Visit Info",
  visit_type: "Visit Type",
  vital_signs: "Vital Signs",
  diet: "Diet",
  pain_assessment: "Pain Assessment",
  sensory: "Sensory",
  neuro: "Neuro",
  respiratory: "Respiratory",
  cardiac: "Cardiac",
  peripheral_circulation: "Peripheral / Circulation",
  genitourinary: "Genitourinary",
  gastrointestinal: "Gastrointestinal",
  endocrine: "Endocrine",
  skin_integrity: "Skin Integrity",
  wound_evaluation: "Wound Evaluation",
  mental_status: "Mental Status",
  functional_status: "Functional Status",
  homebound_status: "Homebound Status",
  patient_caregiver_understanding: "Patient / Caregiver Understanding",
  md_contact: "MD Contact",
};

const textSections = [
  { key: "skilled_nursing", title: "Skilled Nursing" },
  { key: "response_to_intervention", title: "Response to Intervention" },
  { key: "discharge_planning", title: "Discharge Planning" },
  { key: "patient_feedback", title: "Patient / Family Feedback" },
  { key: "narrative", title: "Narrative" },
];

function titleize(value) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const nurseNote = ref(null);
    const patients = ref([]);
    const visits = ref([]);
    const loading = ref(true);
    const error = ref("");

    const patient = computed(() =>
      patients.value.find((candidate) => candidate.id === nurseNote.value?.patient_id)
    );
    const visit = computed(() =>
      visits.value.find((candidate) => candidate.id === nurseNote.value?.visit_id)
    );
    const patientName = computed(() =>
      patient.value
        ? `${patient.value.first_name} ${patient.value.last_name}`
        : nurseNote.value
          ? `Patient #${nurseNote.value.patient_id}`
          : ""
    );
    const clinicalSections = computed(() =>
      Object.entries(clinicalSectionLabels).map(([key, title]) => ({
        key,
        title,
        entries: Object.entries(nurseNote.value?.[key] || {}).filter(
          ([, value]) => value !== "" && value !== null
        ),
      }))
    );

    function formatValue(value) {
      if (Array.isArray(value)) return value.join(", ");
      if (value && typeof value === "object") return JSON.stringify(value);
      if (value === true) return "Yes";
      if (value === false) return "No";
      return value || "Not documented";
    }

    async function loadNurseNote() {
      loading.value = true;
      error.value = "";

      try {
        const [noteResponse, patientResponse, visitResponse] = await Promise.all([
          getNurseNote(props.id),
          listPatients(),
          listVisits(),
        ]);
        nurseNote.value = noteResponse.data;
        patients.value = patientResponse.data;
        visits.value = visitResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadNurseNote);

    return {
      clinicalSections,
      error,
      formatValue,
      loading,
      nurseNote,
      patientName,
      textSections,
      titleize,
      visit,
    };
  },
  template: `
    <div class="page-shell">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/nurse-notes" class="mb-4">
        Nurse Notes
      </v-btn>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <template v-else-if="nurseNote">
        <v-row align="center" class="mb-5">
          <v-col cols="12" md="8">
            <h1 class="text-h4 font-weight-bold mb-2">Nurse Note</h1>
            <div class="text-body-1 text-medium-emphasis">
              {{ patientName }} · {{ visit?.visit_date || 'Visit date not available' }}
            </div>
          </v-col>
          <v-col cols="12" md="4" class="text-md-right">
            <div class="d-flex flex-wrap justify-md-end ga-2">
              <v-btn variant="outlined" prepend-icon="mdi-printer-outline" :to="\`/nurse-notes/\${nurseNote.id}/print\`">
                Print note
              </v-btn>
              <v-btn color="primary" prepend-icon="mdi-pencil-outline" :to="\`/nurse-notes/\${nurseNote.id}/edit\`">
                Edit nurse note
              </v-btn>
            </div>
          </v-col>
        </v-row>

        <v-row class="mb-5">
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Visit and signature</v-card-title>
              <v-list>
                <v-list-item title="Patient" :subtitle="patientName" :to="\`/patients/\${nurseNote.patient_id}\`" />
                <v-list-item title="Visit" :subtitle="visit?.visit_type || 'Not available'" :to="\`/visits/\${nurseNote.visit_id}\`" />
                <v-list-item title="Diagnosis" :subtitle="nurseNote.diagnosis || 'Not provided'" />
                <v-list-item title="Signature date" :subtitle="nurseNote.signature_date || 'Not provided'" />
              </v-list>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Signature Data</v-card-title>
              <v-card-text>{{ nurseNote.signature_data || 'Not provided' }}</v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="section in clinicalSections" :key="section.key" cols="12" md="6">
            <v-card class="mb-5">
              <v-card-title>{{ section.title }}</v-card-title>
              <v-card-text>
                <div v-if="!section.entries.length" class="text-medium-emphasis">Not documented</div>
                <v-list v-else density="compact">
                  <v-list-item
                    v-for="[key, value] in section.entries"
                    :key="key"
                    :title="titleize(key)"
                    :subtitle="formatValue(value)"
                  />
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-for="section in textSections" :key="section.key" class="mb-5">
          <v-card-title>{{ section.title }}</v-card-title>
          <v-card-text>{{ nurseNote[section.key] || 'Not provided' }}</v-card-text>
        </v-card>
      </template>
    </div>
  `,
};
