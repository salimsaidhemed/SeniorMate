import { computed, onMounted, ref } from "vue";

import PatientAvatar from "../components/PatientAvatar.js";
import { getVisitAssessments } from "../services/assessments.js";
import { getVisitAideNote } from "../services/aideNotes.js";
import { getVisitNurseNote } from "../services/nurseNotes.js";
import { listPatients } from "../services/patients.js";
import { getVisit } from "../services/visits.js";

const assessmentLabels = {
  fall_risk: "Fall risk",
  nutrition: "Nutrition",
  mobility: "Mobility",
  cognitive: "Cognitive",
  general: "General",
};

export default {
  components: {
    PatientAvatar,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const visit = ref(null);
    const aideNote = ref(null);
    const nurseNote = ref(null);
    const assessments = ref([]);
    const patients = ref([]);
    const loading = ref(true);
    const error = ref("");

    const patient = computed(() =>
      patients.value.find((candidate) => candidate.id === visit.value?.patient_id)
    );
    const patientName = computed(() =>
      patient.value
        ? `${patient.value.first_name} ${patient.value.last_name}`
        : visit.value
          ? `Patient #${visit.value.patient_id}`
          : ""
    );

    async function loadVisit() {
      loading.value = true;
      error.value = "";

      try {
        const [visitResponse, patientResponse, assessmentResponse] =
          await Promise.all([
          getVisit(props.id),
          listPatients(),
          getVisitAssessments(props.id),
        ]);
        visit.value = visitResponse.data;
        patients.value = patientResponse.data;
        assessments.value = assessmentResponse.data;

        try {
          const aideNoteResponse = await getVisitAideNote(props.id);
          aideNote.value = aideNoteResponse.data;
        } catch (err) {
          if (err.message !== "Aide note not found") {
            throw err;
          }
          aideNote.value = null;
        }

        try {
          const nurseNoteResponse = await getVisitNurseNote(props.id);
          nurseNote.value = nurseNoteResponse.data;
        } catch (err) {
          if (err.message !== "Nurse note not found") {
            throw err;
          }
          nurseNote.value = null;
        }
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadVisit);

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
    <div class="page-shell">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/visits" class="mb-4">
        Visits
      </v-btn>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <template v-else-if="visit">
        <v-row align="center" class="mb-5">
          <v-col cols="12" md="8">
            <div class="d-flex align-center ga-4">
              <PatientAvatar v-if="patient" :patient="patient" :size="60" show-verification />
              <div>
                <h1 class="text-h4 font-weight-bold mb-2">{{ visit.visit_type }}</h1>
                <div class="text-body-1 text-medium-emphasis mb-2">{{ visit.visit_date }} · {{ patientName }}</div>
                <v-chip :color="visit.status === 'completed' ? 'success' : visit.status === 'cancelled' ? 'grey' : 'primary'" size="small">
                  {{ visit.status }}
                </v-chip>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="4">
            <div class="d-flex flex-wrap justify-md-end ga-2">
            <v-btn
              v-if="!aideNote"
              color="primary"
              prepend-icon="mdi-clipboard-plus-outline"
              :to="\`/aide-notes/new?visit_id=\${visit.id}\`"
            >
              Create Aide Note
            </v-btn>
            <v-btn
              v-if="!nurseNote"
              color="secondary"
              prepend-icon="mdi-clipboard-pulse-outline"
              :to="\`/nurse-notes/new?visit_id=\${visit.id}\`"
            >
              Create Nurse Note
            </v-btn>
            <v-btn
              v-if="aideNote"
              color="primary"
              prepend-icon="mdi-clipboard-check-outline"
              :to="\`/aide-notes/\${aideNote.id}\`"
            >
              View Aide Note
            </v-btn>
            <v-btn
              v-if="aideNote"
              color="primary"
              variant="tonal"
              prepend-icon="mdi-pencil-outline"
              :to="\`/aide-notes/\${aideNote.id}/edit\`"
            >
              Edit Aide Note
            </v-btn>
            <v-btn
              v-if="nurseNote"
              color="secondary"
              prepend-icon="mdi-clipboard-pulse-outline"
              :to="\`/nurse-notes/\${nurseNote.id}\`"
            >
              View Nurse Note
            </v-btn>
            <v-btn
              v-if="nurseNote"
              color="secondary"
              variant="tonal"
              prepend-icon="mdi-pencil-outline"
              :to="\`/nurse-notes/\${nurseNote.id}/edit\`"
            >
              Edit Nurse Note
            </v-btn>
            <v-btn
              color="secondary"
              variant="tonal"
              prepend-icon="mdi-clipboard-text-search-outline"
              :to="\`/assessments/new?visit_id=\${visit.id}\`"
            >
              New assessment
            </v-btn>
            <v-btn color="primary" prepend-icon="mdi-pencil-outline" :to="\`/visits/\${visit.id}/edit\`">
              Edit visit
            </v-btn>
            </div>
          </v-col>
        </v-row>

        <v-alert
          :type="aideNote ? 'success' : 'info'"
          variant="tonal"
          class="mb-5"
        >
          {{ aideNote ? 'Aide note completed for this visit.' : 'No aide note has been created for this visit yet.' }}
        </v-alert>

        <v-alert
          :type="nurseNote ? 'success' : 'info'"
          variant="tonal"
          class="mb-5"
        >
          {{ nurseNote ? 'Nurse note completed for this visit.' : 'No nurse note has been created for this visit yet.' }}
        </v-alert>

        <v-row>
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Visit metadata</v-card-title>
              <v-list>
                <v-list-item title="Patient" :subtitle="patientName" :to="\`/patients/\${visit.patient_id}\`" />
                <v-list-item title="Visit date" :subtitle="visit.visit_date || 'Not provided'" />
                <v-list-item title="Visit type" :subtitle="visit.visit_type || 'Not provided'" />
                <v-list-item title="Status" :subtitle="visit.status || 'Not provided'" />
              </v-list>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Staff details</v-card-title>
              <v-list>
                <v-list-item title="Staff name" :subtitle="visit.staff_name || 'Not provided'" />
                <v-list-item title="Staff role" :subtitle="visit.staff_role || 'Not provided'" />
                <v-list-item title="Time in" :subtitle="visit.time_in || 'Not provided'" />
                <v-list-item title="Time out" :subtitle="visit.time_out || 'Not provided'" />
              </v-list>
              <v-divider />
              <v-card-title>Notes</v-card-title>
              <v-card-text>{{ visit.notes || 'Not provided' }}</v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <SectionCard
          title="Visit assessments"
          subtitle="Assessments linked directly to this visit."
          icon="mdi-clipboard-text-search-outline"
          class="mt-5"
        >
          <EmptyState
            v-if="!assessments.length"
            icon="mdi-clipboard-text-outline"
            title="No linked assessments"
            message="Create an assessment with this patient and visit already selected."
          >
            <v-btn
              color="primary"
              :to="\`/assessments/new?visit_id=\${visit.id}\`"
            >
              Create assessment
            </v-btn>
          </EmptyState>
          <v-list v-else lines="two">
            <v-list-item
              v-for="assessment in assessments"
              :key="assessment.id"
              :title="assessmentLabels[assessment.assessment_type] || assessment.assessment_type"
              :subtitle="\`\${assessment.assessment_date} · \${assessment.performed_by || 'Performer not provided'}\`"
              :to="\`/assessments/\${assessment.id}\`"
            >
              <template #append>
                <StatusChip :status="assessment.status" />
              </template>
            </v-list-item>
          </v-list>
        </SectionCard>
      </template>
    </div>
  `,
};
