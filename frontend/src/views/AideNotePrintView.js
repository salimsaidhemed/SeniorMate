import { computed, onMounted, ref } from "vue";

import { getAideNote } from "../services/aideNotes.js";
import { getPatient } from "../services/patients.js";
import { getVisit } from "../services/visits.js";


const sections = [
  ["personal_care", "Personal Care"],
  ["nutrition", "Nutrition"],
  ["mental_status", "Mental Status"],
  ["elimination", "Elimination"],
  ["activity", "Activity"],
  ["assistive_devices", "Assistive Devices"],
  ["housekeeping", "Housekeeping"],
];

export default {
  props: {
    id: { type: String, required: true },
  },
  setup(props) {
    const note = ref(null);
    const patient = ref(null);
    const visit = ref(null);
    const loading = ref(true);
    const error = ref("");
    const patientName = computed(() =>
      patient.value
        ? `${patient.value.first_name} ${patient.value.last_name}`
        : "Patient"
    );

    async function loadReport() {
      loading.value = true;
      error.value = "";
      try {
        const noteResponse = await getAideNote(props.id);
        note.value = noteResponse.data;
        const [patientResponse, visitResponse] = await Promise.all([
          getPatient(note.value.patient_id),
          getVisit(note.value.visit_id),
        ]);
        patient.value = patientResponse.data;
        visit.value = visitResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadReport);
    return { error, loading, note, patientName, sections, visit };
  },
  template: `
    <div class="page-shell print-route">
      <ErrorAlert :message="error" />
      <LoadingState v-if="loading" label="Loading aide note" />
      <PrintPageLayout
        v-else-if="note && visit"
        title="Home Health Aide Note"
        :subtitle="\`\${patientName} · \${visit.visit_date}\`"
        :back-to="\`/aide-notes/\${note.id}\`"
      >
        <PrintSection title="Patient and Visit">
          <div class="print-grid print-grid--3">
            <PrintField label="Patient" :value="patientName" />
            <PrintField label="Visit date" :value="visit.visit_date" />
            <PrintField label="Visit type" :value="visit.visit_type" />
            <PrintField label="Aide name" :value="note.aide_name" />
            <PrintField label="Time in" :value="note.time_in" />
            <PrintField label="Time out" :value="note.time_out" />
          </div>
        </PrintSection>

        <div class="print-grid print-grid--2">
          <PrintSection v-for="[key, title] in sections" :key="key" :title="title">
            <ChecklistSummary :data="note[key]" />
          </PrintSection>
        </div>

        <PrintSection title="Additional Notes">
          <p>{{ note.additional_notes || 'No additional notes recorded.' }}</p>
        </PrintSection>

        <PrintSection title="Signature / Staff Details">
          <SignatureBlock
            :name="note.aide_name"
            :date="note.signature_date"
            :signature-data="note.signature_data"
            role-label="Aide name"
          />
        </PrintSection>
      </PrintPageLayout>
    </div>
  `,
};
