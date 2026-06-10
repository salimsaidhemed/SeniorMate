import { computed, onMounted, ref } from "vue";

import PatientAvatar from "../components/PatientAvatar.js";
import { getPatientAssessments } from "../services/assessments.js";
import { getPatientMedicalRecords } from "../services/medicalRecords.js";
import { getPatient } from "../services/patients.js";
import { listPatientVisits } from "../services/visits.js";


const assessmentLabels = {
  fall_risk: "Fall risk",
  nutrition: "Nutrition",
  mobility: "Mobility",
  cognitive: "Cognitive",
  general: "General",
};

export default {
  components: { PatientAvatar },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const patient = ref(null);
    const visits = ref([]);
    const assessments = ref([]);
    const medicalRecords = ref([]);
    const loading = ref(true);
    const error = ref("");

    const patientName = computed(() =>
      patient.value
        ? `${patient.value.first_name} ${patient.value.last_name}`
        : "Patient"
    );
    const recentVisits = computed(() => visits.value.slice(0, 5));
    const recentAssessments = computed(() => assessments.value.slice(0, 5));
    const recentRecords = computed(() => medicalRecords.value.slice(0, 5));

    async function loadReport() {
      loading.value = true;
      error.value = "";
      try {
        const [patientResponse, visitResponse, assessmentResponse, recordResponse] =
          await Promise.all([
            getPatient(props.id),
            listPatientVisits(props.id),
            getPatientAssessments(props.id),
            getPatientMedicalRecords(props.id),
          ]);
        patient.value = patientResponse.data;
        visits.value = visitResponse.data;
        assessments.value = assessmentResponse.data;
        medicalRecords.value = recordResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadReport);

    return {
      assessmentLabels,
      error,
      loading,
      patient,
      patientName,
      recentAssessments,
      recentRecords,
      recentVisits,
    };
  },
  template: `
    <div class="page-shell print-route">
      <ErrorAlert :message="error" />
      <LoadingState v-if="loading" label="Loading patient summary" />

      <PrintPageLayout
        v-else-if="patient"
        title="Patient Summary"
        :subtitle="patientName"
        :back-to="\`/patients/\${patient.id}\`"
      >
        <div class="print-profile">
          <PatientAvatar :patient="patient" :size="84" />
          <div>
            <h2>{{ patientName }}</h2>
            <div class="print-status">{{ patient.status }}</div>
          </div>
        </div>

        <PrintSection title="Demographics">
          <div class="print-grid print-grid--3">
            <PrintField label="Date of birth" :value="patient.date_of_birth" />
            <PrintField label="Gender" :value="patient.gender" />
            <PrintField label="Phone" :value="patient.phone" />
            <PrintField label="Email" :value="patient.email" />
            <PrintField label="Address" :value="patient.address" />
            <PrintField label="Status" :value="patient.status" />
          </div>
        </PrintSection>

        <div class="print-grid print-grid--2">
          <PrintSection title="Emergency Contact">
            <PrintField label="Name" :value="patient.emergency_contact_name" />
            <PrintField label="Phone" :value="patient.emergency_contact_phone" />
          </PrintSection>
          <PrintSection title="Diagnosis Summary">
            <p>{{ patient.diagnosis_summary || 'Not provided' }}</p>
          </PrintSection>
        </div>

        <PrintSection title="Recent Visits" subtitle="Up to five most recent visits">
          <table v-if="recentVisits.length" class="print-table">
            <thead>
              <tr><th>Date</th><th>Visit type</th><th>Staff</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr v-for="visit in recentVisits" :key="visit.id">
                <td>{{ visit.visit_date }}</td>
                <td>{{ visit.visit_type }}</td>
                <td>{{ visit.staff_name || 'Not provided' }}</td>
                <td>{{ visit.status }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="print-empty">No visits recorded.</p>
        </PrintSection>

        <PrintSection title="Recent Assessments" subtitle="Up to five most recent assessments">
          <table v-if="recentAssessments.length" class="print-table">
            <thead>
              <tr><th>Date</th><th>Type</th><th>Performed by</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr v-for="assessment in recentAssessments" :key="assessment.id">
                <td>{{ assessment.assessment_date }}</td>
                <td>{{ assessmentLabels[assessment.assessment_type] || assessment.assessment_type }}</td>
                <td>{{ assessment.performed_by || 'Not provided' }}</td>
                <td>{{ assessment.status }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="print-empty">No assessments recorded.</p>
        </PrintSection>

        <PrintSection title="Recent Medical Records" subtitle="Metadata only; uploaded files are not embedded">
          <table v-if="recentRecords.length" class="print-table">
            <thead>
              <tr><th>Title</th><th>Record type</th><th>File name</th><th>Uploaded</th></tr>
            </thead>
            <tbody>
              <tr v-for="record in recentRecords" :key="record.id">
                <td>{{ record.title }}</td>
                <td>{{ record.record_type || 'Not provided' }}</td>
                <td>{{ record.file_name }}</td>
                <td>{{ record.uploaded_at?.slice(0, 10) || 'Not provided' }}</td>
              </tr>
            </tbody>
          </table>
          <p v-else class="print-empty">No medical records uploaded.</p>
        </PrintSection>
      </PrintPageLayout>
    </div>
  `,
};
