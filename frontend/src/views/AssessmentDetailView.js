import { computed, onMounted, ref } from "vue";

import { getAssessment } from "../services/assessments.js";
import { getPatient } from "../services/patients.js";
import { getVisit } from "../services/visits.js";


const assessmentLabels = {
  fall_risk: "Fall risk",
  nutrition: "Nutrition",
  mobility: "Mobility",
  cognitive: "Cognitive",
  general: "General",
};

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
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
    const title = computed(() =>
      assessment.value
        ? `${assessmentLabels[assessment.value.assessment_type] || assessment.value.assessment_type} assessment`
        : "Assessment"
    );
    const findingRows = computed(() => {
      const findings = assessment.value?.findings;
      if (!findings) return [];
      if (Array.isArray(findings)) {
        return findings.map((value, index) => ({
          label: `Item ${index + 1}`,
          value: typeof value === "object" ? JSON.stringify(value) : String(value),
        }));
      }
      return Object.entries(findings).map(([key, value]) => ({
        label: key.replaceAll("_", " "),
        value: typeof value === "object" ? JSON.stringify(value) : String(value),
      }));
    });

    async function loadAssessment() {
      loading.value = true;
      error.value = "";
      try {
        const assessmentResponse = await getAssessment(props.id);
        assessment.value = assessmentResponse.data;

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

    onMounted(loadAssessment);

    return {
      assessment,
      error,
      findingRows,
      loading,
      patientName,
      title,
      visit,
    };
  },
  template: `
    <div class="page-shell">
      <v-btn
        variant="text"
        prepend-icon="mdi-arrow-left"
        :to="assessment ? \`/patients/\${assessment.patient_id}\` : '/patients'"
        class="mb-4"
      >
        Patient record
      </v-btn>

      <ErrorAlert :message="error" />
      <LoadingState v-if="loading" label="Loading assessment" />

      <template v-else-if="assessment">
        <PageHeader
          :title="title"
          :subtitle="\`\${patientName} · \${assessment.assessment_date}\`"
          icon="mdi-clipboard-text-search-outline"
        >
          <template #actions>
            <v-btn
              variant="outlined"
              prepend-icon="mdi-printer-outline"
              :to="\`/assessments/\${assessment.id}/print\`"
            >
              Print assessment
            </v-btn>
            <v-btn
              color="primary"
              prepend-icon="mdi-pencil-outline"
              :to="\`/assessments/\${assessment.id}/edit\`"
            >
              Edit assessment
            </v-btn>
          </template>
        </PageHeader>

        <v-row class="mb-5">
          <v-col cols="12" md="6">
            <SectionCard title="Assessment details" icon="mdi-information-outline">
              <v-list>
                <v-list-item title="Patient" :subtitle="patientName" :to="\`/patients/\${assessment.patient_id}\`" />
                <v-list-item
                  title="Related visit"
                  :subtitle="visit ? \`\${visit.visit_date} · \${visit.visit_type}\` : 'Not linked to a visit'"
                  :to="visit ? \`/visits/\${visit.id}\` : undefined"
                />
                <v-list-item title="Performed by" :subtitle="assessment.performed_by || 'Not provided'" />
                <v-list-item title="Assessment date" :subtitle="assessment.assessment_date" />
              </v-list>
              <StatusChip :status="assessment.status" class="ma-4 mt-0" />
            </SectionCard>
          </v-col>
          <v-col cols="12" md="6">
            <SectionCard title="Summary" icon="mdi-text-box-outline">
              <div class="text-body-1 mb-5">
                {{ assessment.summary || 'No summary provided.' }}
              </div>
              <div class="text-subtitle-1 font-weight-medium mb-2">Recommendations</div>
              <div class="text-body-1">
                {{ assessment.recommendations || 'No recommendations provided.' }}
              </div>
            </SectionCard>
          </v-col>
        </v-row>

        <SectionCard title="Findings" icon="mdi-magnify-scan">
          <EmptyState
            v-if="!findingRows.length"
            icon="mdi-clipboard-text-outline"
            title="No findings recorded"
            message="Edit this assessment to add structured findings."
          />
          <v-list v-else lines="two">
            <v-list-item
              v-for="finding in findingRows"
              :key="finding.label"
              :title="finding.label"
              :subtitle="finding.value"
            />
          </v-list>
        </SectionCard>
      </template>
    </div>
  `,
};
