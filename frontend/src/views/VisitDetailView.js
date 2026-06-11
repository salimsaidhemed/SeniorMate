import { computed, onMounted, ref } from "vue";

import PatientAvatar from "../components/PatientAvatar.js";
import {
  canCreateAideNote,
  canCreateNurseNote,
  canManageAssessments,
  canManageVisits,
  canViewReports,
} from "../permissions.js";
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
      canCreateAideNote,
      canCreateNurseNote,
      canManageAssessments,
      canManageVisits,
      canViewReports,
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
        <DetailHeader
          eyebrow="Visit record"
          :title="visit.visit_type"
          :subtitle="\`\${visit.visit_date} · \${patientName}\`"
        >
          <template #avatar>
            <PatientAvatar v-if="patient" :patient="patient" :size="68" show-verification />
          </template>
          <template #meta>
            <StatusChip :status="visit.status" />
            <v-chip size="small" variant="outlined" prepend-icon="mdi-account-badge-outline">
              {{ visit.staff_role || 'Staff role not provided' }}
            </v-chip>
            <v-chip v-if="visit.time_in || visit.time_out" size="small" variant="outlined" prepend-icon="mdi-clock-outline">
              {{ visit.time_in || '—' }} – {{ visit.time_out || '—' }}
            </v-chip>
          </template>
          <template #actions>
            <v-btn variant="outlined" prepend-icon="mdi-account-outline" :to="\`/patients/\${visit.patient_id}\`">
              Patient
            </v-btn>
            <v-btn v-if="canViewReports()" variant="outlined" prepend-icon="mdi-printer-outline" :to="\`/visits/\${visit.id}/print\`">
              Print summary
            </v-btn>
            <v-btn v-if="canManageVisits()" color="primary" prepend-icon="mdi-pencil-outline" :to="\`/visits/\${visit.id}/edit\`">
              Edit visit
            </v-btn>
          </template>
        </DetailHeader>

        <SectionCard
          title="Care documentation"
          subtitle="Complete or review the clinical records linked to this visit."
          icon="mdi-clipboard-text-multiple-outline"
          class="mb-5"
        >
          <div class="documentation-actions">
            <v-btn
              v-if="!aideNote && canCreateAideNote()"
              class="documentation-action"
              color="primary"
              variant="tonal"
              prepend-icon="mdi-clipboard-plus-outline"
              :to="\`/aide-notes/new?visit_id=\${visit.id}\`"
            >
              Create aide note
            </v-btn>
            <v-btn
              v-if="!nurseNote && canCreateNurseNote()"
              class="documentation-action"
              color="secondary"
              variant="tonal"
              prepend-icon="mdi-clipboard-pulse-outline"
              :to="\`/nurse-notes/new?visit_id=\${visit.id}\`"
            >
              Create nurse note
            </v-btn>
            <v-btn
              v-if="aideNote"
              class="documentation-action"
              color="primary"
              variant="tonal"
              prepend-icon="mdi-clipboard-check-outline"
              :to="\`/aide-notes/\${aideNote.id}\`"
            >
              View aide note
            </v-btn>
            <v-btn
              v-if="nurseNote"
              class="documentation-action"
              color="secondary"
              variant="tonal"
              prepend-icon="mdi-clipboard-pulse-outline"
              :to="\`/nurse-notes/\${nurseNote.id}\`"
            >
              View nurse note
            </v-btn>
            <v-btn
              v-if="canManageAssessments()"
              class="documentation-action"
              color="secondary"
              variant="tonal"
              prepend-icon="mdi-clipboard-text-search-outline"
              :to="\`/assessments/new?visit_id=\${visit.id}\`"
            >
              New assessment
            </v-btn>
            <v-btn
              v-if="aideNote && canCreateAideNote()"
              class="documentation-action"
              variant="outlined"
              prepend-icon="mdi-pencil-outline"
              :to="\`/aide-notes/\${aideNote.id}/edit\`"
            >
              Edit aide note
            </v-btn>
            <v-btn
              v-if="nurseNote && canCreateNurseNote()"
              class="documentation-action"
              variant="outlined"
              prepend-icon="mdi-pencil-outline"
              :to="\`/nurse-notes/\${nurseNote.id}/edit\`"
            >
              Edit nurse note
            </v-btn>
          </div>
        </SectionCard>

        <v-row class="detail-grid">
          <v-col cols="12" md="6">
            <SectionCard title="Visit details" icon="mdi-calendar-text-outline">
              <v-list>
                <v-list-item title="Patient" :subtitle="patientName" :to="\`/patients/\${visit.patient_id}\`" />
                <v-list-item title="Visit date" :subtitle="visit.visit_date || 'Not provided'" />
                <v-list-item title="Visit type" :subtitle="visit.visit_type || 'Not provided'" />
                <v-list-item title="Status" :subtitle="visit.status || 'Not provided'" />
              </v-list>
            </SectionCard>
          </v-col>

          <v-col cols="12" md="6">
            <SectionCard title="Staff and notes" icon="mdi-account-badge-outline">
              <v-list>
                <v-list-item title="Staff name" :subtitle="visit.staff_name || 'Not provided'" />
                <v-list-item title="Staff role" :subtitle="visit.staff_role || 'Not provided'" />
                <v-list-item title="Time in" :subtitle="visit.time_in || 'Not provided'" />
                <v-list-item title="Time out" :subtitle="visit.time_out || 'Not provided'" />
              </v-list>
              <v-divider />
              <div class="text-subtitle-2 mt-4 mb-2">Visit notes</div>
              <div class="text-body-2 text-medium-emphasis">{{ visit.notes || 'Not provided' }}</div>
            </SectionCard>
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
              v-if="canManageAssessments()"
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
