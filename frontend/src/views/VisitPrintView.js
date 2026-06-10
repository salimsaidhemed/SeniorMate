import { computed, onMounted, ref } from "vue";

import PatientAvatar from "../components/PatientAvatar.js";
import { getVisitAssessments } from "../services/assessments.js";
import { getVisitAideNote } from "../services/aideNotes.js";
import { getVisitNurseNote } from "../services/nurseNotes.js";
import { getPatient } from "../services/patients.js";
import { getVisit } from "../services/visits.js";


const assessmentLabels = {
  fall_risk: "Fall risk",
  nutrition: "Nutrition",
  mobility: "Mobility",
  cognitive: "Cognitive",
  general: "General",
};

async function optionalRequest(request) {
  try {
    return (await request()).data;
  } catch (err) {
    if (err.message.toLowerCase().includes("not found")) return null;
    throw err;
  }
}

export default {
  components: { PatientAvatar },
  props: {
    id: { type: String, required: true },
  },
  setup(props) {
    const visit = ref(null);
    const patient = ref(null);
    const aideNote = ref(null);
    const nurseNote = ref(null);
    const assessments = ref([]);
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
        const visitResponse = await getVisit(props.id);
        visit.value = visitResponse.data;
        const [patientResponse, assessmentResponse, aide, nurse] =
          await Promise.all([
            getPatient(visit.value.patient_id),
            getVisitAssessments(props.id),
            optionalRequest(() => getVisitAideNote(props.id)),
            optionalRequest(() => getVisitNurseNote(props.id)),
          ]);
        patient.value = patientResponse.data;
        assessments.value = assessmentResponse.data;
        aideNote.value = aide;
        nurseNote.value = nurse;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadReport);
    return {
      aideNote,
      assessments,
      assessmentLabels,
      error,
      loading,
      nurseNote,
      patient,
      patientName,
      visit,
    };
  },
  template: `
    <div class="page-shell print-route">
      <ErrorAlert :message="error" />
      <LoadingState v-if="loading" label="Loading visit summary" />
      <PrintPageLayout
        v-else-if="visit && patient"
        title="Visit Summary"
        :subtitle="\`\${visit.visit_date} · \${visit.visit_type}\`"
        :back-to="\`/visits/\${visit.id}\`"
      >
        <div class="print-profile">
          <PatientAvatar :patient="patient" :size="72" />
          <div>
            <h2>{{ patientName }}</h2>
            <p>{{ patient.date_of_birth || 'Date of birth not provided' }}</p>
          </div>
        </div>

        <PrintSection title="Visit Details">
          <div class="print-grid print-grid--3">
            <PrintField label="Visit date" :value="visit.visit_date" />
            <PrintField label="Visit type" :value="visit.visit_type" />
            <PrintField label="Status" :value="visit.status" />
            <PrintField label="Staff name" :value="visit.staff_name" />
            <PrintField label="Staff role" :value="visit.staff_role" />
            <PrintField label="Time" :value="\`\${visit.time_in || 'Not set'} – \${visit.time_out || 'Not set'}\`" />
          </div>
        </PrintSection>

        <PrintSection title="Visit Notes">
          <p>{{ visit.notes || 'No visit notes recorded.' }}</p>
        </PrintSection>

        <PrintSection title="Care Note Status">
          <div class="print-grid print-grid--2">
            <PrintField label="Aide note" :value="aideNote ? 'Completed' : 'Not recorded'" />
            <PrintField label="Nurse note" :value="nurseNote ? 'Completed' : 'Not recorded'" />
          </div>
        </PrintSection>

        <PrintSection title="Linked Assessments">
          <table v-if="assessments.length" class="print-table">
            <thead>
              <tr><th>Date</th><th>Type</th><th>Performed by</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr v-for="assessment in assessments" :key="assessment.id">
                <td>{{ assessment.assessment_date }}</td>
                <td>{{ assessmentLabels[assessment.assessment_type] || assessment.assessment_type }}</td>
                <td>{{ assessment.performed_by || 'Not provided' }}</td>
                <td>{{ assessment.status }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="print-empty">No assessments linked to this visit.</p>
        </PrintSection>
      </PrintPageLayout>
    </div>
  `,
};
