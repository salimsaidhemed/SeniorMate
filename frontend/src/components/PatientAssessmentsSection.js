import { onMounted, ref } from "vue";

import {
  deleteAssessment,
  getPatientAssessments,
} from "../services/assessments.js";
import { canManageAssessments } from "../permissions.js";


const assessmentLabels = {
  fall_risk: "Fall risk",
  nutrition: "Nutrition",
  mobility: "Mobility",
  cognitive: "Cognitive",
  general: "General",
};

export default {
  props: {
    patientId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const assessments = ref([]);
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const confirmDelete = ref(false);
    const deleting = ref(false);
    const selectedAssessment = ref(null);

    const headers = [
      { title: "Date", key: "assessment_date" },
      { title: "Type", key: "assessment_type" },
      { title: "Performed by", key: "performed_by" },
      { title: "Status", key: "status" },
      { title: "Actions", key: "actions", sortable: false },
    ];

    async function loadAssessments() {
      loading.value = true;
      error.value = "";
      try {
        const response = await getPatientAssessments(props.patientId);
        assessments.value = response.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function askDelete(assessment) {
      selectedAssessment.value = assessment;
      confirmDelete.value = true;
    }

    async function removeAssessment() {
      if (!selectedAssessment.value) return;

      deleting.value = true;
      error.value = "";
      success.value = "";
      try {
        await deleteAssessment(selectedAssessment.value.id);
        confirmDelete.value = false;
        selectedAssessment.value = null;
        success.value = "Assessment deleted successfully.";
        await loadAssessments();
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    function assessmentLabel(value) {
      return assessmentLabels[value] || value;
    }

    onMounted(loadAssessments);

    return {
      assessmentLabel,
      assessments,
      askDelete,
      canManageAssessments,
      confirmDelete,
      deleting,
      error,
      headers,
      loading,
      removeAssessment,
      selectedAssessment,
      success,
    };
  },
  template: `
    <SectionCard
      title="Assessments"
      subtitle="Structured clinical and care assessments for this patient."
      icon="mdi-clipboard-text-search-outline"
      class="data-card mb-6"
    >
      <div v-if="canManageAssessments()" class="d-flex flex-wrap justify-end ga-3 mb-4">
        <v-btn
          color="primary"
          prepend-icon="mdi-clipboard-plus-outline"
          :to="\`/assessments/new?patient_id=\${patientId}\`"
        >
          New assessment
        </v-btn>
      </div>

      <ErrorAlert :message="error" />
      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        {{ success }}
      </v-alert>

      <LoadingState v-if="loading" label="Loading assessments" />

      <v-data-table
        v-else
        :headers="headers"
        :items="assessments"
        item-value="id"
      >
        <template #no-data>
          <EmptyState
            icon="mdi-clipboard-text-outline"
            title="No assessments yet"
            message="Create the first structured assessment for this patient."
          >
            <v-btn
              v-if="canManageAssessments()"
              color="primary"
              :to="\`/assessments/new?patient_id=\${patientId}\`"
            >
              Create assessment
            </v-btn>
          </EmptyState>
        </template>

        <template #[\`item.assessment_type\`]="{ item }">
          {{ assessmentLabel(item.assessment_type) }}
        </template>

        <template #[\`item.performed_by\`]="{ item }">
          {{ item.performed_by || 'Not provided' }}
        </template>

        <template #[\`item.status\`]="{ item }">
          <StatusChip :status="item.status" />
        </template>

        <template #[\`item.actions\`]="{ item }">
          <v-btn
            icon="mdi-eye-outline"
            variant="text"
            :to="\`/assessments/\${item.id}\`"
            aria-label="View assessment"
          />
          <v-btn
            v-if="canManageAssessments()"
            icon="mdi-pencil-outline"
            variant="text"
            :to="\`/assessments/\${item.id}/edit\`"
            aria-label="Edit assessment"
          />
          <v-btn
            v-if="canManageAssessments()"
            icon="mdi-delete-outline"
            variant="text"
            color="error"
            aria-label="Delete assessment"
            @click="askDelete(item)"
          />
        </template>
      </v-data-table>

      <ConfirmDialog
        v-if="canManageAssessments()"
        v-model="confirmDelete"
        title="Delete assessment"
        :message="\`Delete this \${assessmentLabel(selectedAssessment?.assessment_type || '')} assessment?\`"
        :loading="deleting"
        @confirm="removeAssessment"
      />
    </SectionCard>
  `,
};
