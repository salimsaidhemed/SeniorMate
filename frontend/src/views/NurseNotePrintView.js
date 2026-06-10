import { computed, onMounted, ref } from "vue";

import { getNurseNote } from "../services/nurseNotes.js";
import { getPatient } from "../services/patients.js";
import { getVisit } from "../services/visits.js";


const clinicalSections = [
  ["living_arrangements", "Living Arrangements"],
  ["visit_type", "Visit Type"],
  ["vital_signs", "Vital Signs"],
  ["diet", "Diet"],
  ["pain_assessment", "Pain Assessment"],
  ["sensory", "Sensory"],
  ["neuro", "Neurological"],
  ["respiratory", "Respiratory"],
  ["cardiac", "Cardiac"],
  ["peripheral_circulation", "Peripheral / Circulation"],
  ["genitourinary", "Genitourinary"],
  ["gastrointestinal", "Gastrointestinal"],
  ["endocrine", "Endocrine"],
  ["skin_integrity", "Skin Integrity"],
  ["wound_evaluation", "Wound Evaluation"],
  ["mental_status", "Mental Status"],
  ["functional_status", "Functional Status"],
  ["homebound_status", "Homebound Status"],
  ["patient_caregiver_understanding", "Patient / Caregiver Understanding"],
  ["md_contact", "MD Contact"],
];

const narrativeSections = [
  ["skilled_nursing", "Skilled Nursing"],
  ["response_to_intervention", "Response to Intervention"],
  ["discharge_planning", "Discharge Planning"],
  ["patient_feedback", "Patient / Family Feedback"],
  ["narrative", "Narrative"],
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
        const noteResponse = await getNurseNote(props.id);
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
    return {
      clinicalSections,
      error,
      loading,
      narrativeSections,
      note,
      patientName,
      visit,
    };
  },
  template: `
    <div class="page-shell print-route">
      <ErrorAlert :message="error" />
      <LoadingState v-if="loading" label="Loading nurse note" />
      <PrintPageLayout
        v-else-if="note && visit"
        title="Nurses Progress Note"
        :subtitle="\`\${patientName} · \${visit.visit_date}\`"
        :back-to="\`/nurse-notes/\${note.id}\`"
      >
        <PrintSection title="Patient / Visit Information">
          <div class="print-grid print-grid--3">
            <PrintField label="Patient" :value="patientName" />
            <PrintField label="Visit date" :value="visit.visit_date" />
            <PrintField label="Visit type" :value="visit.visit_type" />
            <PrintField label="Diagnosis" :value="note.diagnosis" />
            <PrintField label="Staff" :value="visit.staff_name" />
            <PrintField label="Staff role" :value="visit.staff_role" />
          </div>
        </PrintSection>

        <div class="print-grid print-grid--2">
          <PrintSection
            v-for="[key, title] in clinicalSections"
            :key="key"
            :title="title"
          >
            <ChecklistSummary :data="note[key]" />
          </PrintSection>
        </div>

        <PrintSection
          v-for="[key, title] in narrativeSections"
          :key="key"
          :title="title"
        >
          <p>{{ note[key] || 'Not documented' }}</p>
        </PrintSection>

        <PrintSection title="Signature">
          <SignatureBlock
            :name="visit.staff_name"
            :date="note.signature_date"
            :signature-data="note.signature_data"
            role-label="RN / LPN"
          />
        </PrintSection>
      </PrintPageLayout>
    </div>
  `,
};
