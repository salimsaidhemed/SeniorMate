import { computed, onMounted, ref } from "vue";

import { getAssessment } from "../services/assessments.js";
import { getPatient } from "../services/patients.js";
import { getVisit } from "../services/visits.js";


const assessmentLabels = {
  fall_risk: "Fall Risk",
  nutrition: "Nutrition",
  mobility: "Mobility",
  cognitive: "Cognitive",
  general: "General",
};

export default {
  props: {
    id: { type: String, required: true },
  },
  setup(props) {
    const assessment = ref(null);
    const patient = ref(null);
    const visit = ref(null);
    const loading = ref(true);
    const error = ref("");
    const patientName = computed(() =>
      patient.value
        ? `${patient.value.first_name} ${patient.value.last_name}`
        : "Patient"
    );
    const assessmentName = computed(() =>
      assessment.value
        ? assessmentLabels[assessment.value.assessment_type] ||
          assessment.value.assessment_type
        : "Assessment"
    );

    async function loadReport() {
      loading.value = true;
      error.value = "";
      try {
        const response = await getAssessment(props.id);
        assessment.value = response.data;
        const requests = [getPatient(assessment.value.patient_id)];
        if (assessment.value.visit_id) {
          requests.push(getVisit(assessment.value.visit_id));
        }
        const [patientResponse, visitResponse] = await Promise.all(requests);
        patient.value = patientResponse.data;
        visit.value = visitResponse?.data || null;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadReport);
    return {
      assessment,
      assessmentName,
      error,
      loading,
      patientName,
      visit,
    };
  },
  template: `
    <div class="page-shell print-route">
      <ErrorAlert :message="error" />
      <LoadingState v-if="loading" label="Loading assessment report" />
      <PrintPageLayout
        v-else-if="assessment"
        :title="\`\${assessmentName} Assessment\`"
        :subtitle="patientName"
        :back-to="\`/assessments/\${assessment.id}\`"
      >
        <PrintSection title="Assessment Details">
          <div class="print-grid print-grid--3">
            <PrintField label="Patient" :value="patientName" />
            <PrintField label="Assessment type" :value="assessmentName" />
            <PrintField label="Assessment date" :value="assessment.assessment_date" />
            <PrintField label="Performed by" :value="assessment.performed_by" />
            <PrintField label="Status" :value="assessment.status" />
            <PrintField
              label="Related visit"
              :value="visit ? \`\${visit.visit_date} · \${visit.visit_type}\` : 'Not linked'"
            />
          </div>
        </PrintSection>

        <PrintSection title="Summary">
          <p>{{ assessment.summary || 'No summary provided.' }}</p>
        </PrintSection>

        <PrintSection title="Findings">
          <ChecklistSummary :data="assessment.findings" empty-text="No findings recorded." />
        </PrintSection>

        <PrintSection title="Recommendations">
          <p>{{ assessment.recommendations || 'No recommendations provided.' }}</p>
        </PrintSection>
      </PrintPageLayout>
    </div>
  `,
};
