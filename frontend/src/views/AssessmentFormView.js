import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import {
  createAssessment,
  getAssessment,
  updateAssessment,
} from "../services/assessments.js";
import { listPatients } from "../services/patients.js";
import { getVisit, listVisits } from "../services/visits.js";


const emptyForm = () => ({
  patient_id: null,
  visit_id: null,
  assessment_type: "general",
  assessment_date: new Date().toISOString().slice(0, 10),
  performed_by: "",
  summary: "",
  findings: "{}",
  recommendations: "",
  status: "draft",
});

export default {
  props: {
    mode: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const form = ref(emptyForm());
    const patients = ref([]);
    const visits = ref([]);
    const loading = ref(true);
    const saving = ref(false);
    const error = ref("");
    const errors = ref({});

    const isEdit = computed(() => props.mode === "edit");
    const title = computed(() =>
      isEdit.value ? "Edit assessment" : "New assessment"
    );
    const patientOptions = computed(() =>
      patients.value.map((patient) => ({
        title: `${patient.first_name} ${patient.last_name}`,
        value: patient.id,
      }))
    );
    const visitOptions = computed(() =>
      visits.value
        .filter((visit) => visit.patient_id === Number(form.value.patient_id))
        .map((visit) => ({
          title: `${visit.visit_date} · ${visit.visit_type}`,
          value: visit.id,
        }))
    );
    const assessmentTypes = [
      { title: "Fall risk", value: "fall_risk" },
      { title: "Nutrition", value: "nutrition" },
      { title: "Mobility", value: "mobility" },
      { title: "Cognitive", value: "cognitive" },
      { title: "General", value: "general" },
    ];
    const statusOptions = [
      { title: "Draft", value: "draft" },
      { title: "Completed", value: "completed" },
    ];

    function validate() {
      const nextErrors = {};
      if (!form.value.patient_id) nextErrors.patient_id = "Patient is required.";
      if (!form.value.assessment_type) {
        nextErrors.assessment_type = "Assessment type is required.";
      }
      if (!form.value.assessment_date) {
        nextErrors.assessment_date = "Assessment date is required.";
      }

      try {
        const findings = JSON.parse(form.value.findings || "{}");
        if (
          findings !== null &&
          typeof findings !== "object"
        ) {
          nextErrors.findings = "Findings must be a JSON object or array.";
        }
      } catch {
        nextErrors.findings = "Enter valid JSON findings.";
      }

      errors.value = nextErrors;
      return Object.keys(nextErrors).length === 0;
    }

    function payload() {
      return {
        patient_id: Number(form.value.patient_id),
        visit_id: form.value.visit_id ? Number(form.value.visit_id) : null,
        assessment_type: form.value.assessment_type,
        assessment_date: form.value.assessment_date,
        performed_by: form.value.performed_by || null,
        summary: form.value.summary || null,
        findings: JSON.parse(form.value.findings || "{}"),
        recommendations: form.value.recommendations || null,
        status: form.value.status,
      };
    }

    async function loadForm() {
      loading.value = true;
      error.value = "";
      try {
        const [patientResponse, visitResponse] = await Promise.all([
          listPatients(),
          listVisits(),
        ]);
        patients.value = patientResponse.data;
        visits.value = visitResponse.data;

        if (isEdit.value) {
          const response = await getAssessment(route.params.id);
          const assessment = response.data;
          form.value = {
            ...emptyForm(),
            ...assessment,
            findings: JSON.stringify(assessment.findings || {}, null, 2),
          };
        } else if (route.query.visit_id) {
          const response = await getVisit(route.query.visit_id);
          form.value.patient_id = response.data.patient_id;
          form.value.visit_id = response.data.id;
          form.value.assessment_date = response.data.visit_date;
          form.value.performed_by = response.data.staff_name || "";
        } else if (route.query.patient_id) {
          form.value.patient_id = Number(route.query.patient_id);
        }
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    async function submit() {
      error.value = "";
      if (!validate()) return;

      saving.value = true;
      try {
        const response = isEdit.value
          ? await updateAssessment(route.params.id, payload())
          : await createAssessment(payload());
        await router.push(`/assessments/${response.data.id}`);
      } catch (err) {
        error.value = err.message;
        errors.value = err.payload?.errors || errors.value;
      } finally {
        saving.value = false;
      }
    }

    watch(
      () => form.value.patient_id,
      (patientId, previousPatientId) => {
        if (
          previousPatientId &&
          patientId !== previousPatientId &&
          !visitOptions.value.some((visit) => visit.value === form.value.visit_id)
        ) {
          form.value.visit_id = null;
        }
      }
    );

    onMounted(loadForm);

    return {
      assessmentTypes,
      error,
      errors,
      form,
      isEdit,
      loading,
      patientOptions,
      saving,
      statusOptions,
      submit,
      title,
      visitOptions,
    };
  },
  template: `
    <div class="page-shell">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" :to="form.patient_id ? \`/patients/\${form.patient_id}\` : '/patients'" class="mb-4">
        Patient record
      </v-btn>

      <PageHeader
        :title="title"
        subtitle="Record structured findings and practical care recommendations."
        icon="mdi-clipboard-text-search-outline"
      />

      <ErrorAlert :message="error" />
      <LoadingState v-if="loading" label="Loading assessment" />

      <v-form v-else @submit.prevent="submit">
        <SectionCard title="Assessment details" icon="mdi-clipboard-outline" class="mb-5">
          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="form.patient_id"
                label="Patient *"
                :items="patientOptions"
                :error-messages="errors.patient_id"
                required
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                v-model="form.visit_id"
                label="Related visit"
                :items="visitOptions"
                clearable
                hint="Optional. Only visits for the selected patient are shown."
                persistent-hint
                :error-messages="errors.visit_id"
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="form.assessment_type"
                label="Assessment type *"
                :items="assessmentTypes"
                :error-messages="errors.assessment_type"
                required
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="form.assessment_date"
                label="Assessment date *"
                type="date"
                :error-messages="errors.assessment_date"
                required
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="form.status"
                label="Status"
                :items="statusOptions"
                :error-messages="errors.status"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="form.performed_by"
                label="Performed by"
                placeholder="Name and role"
              />
            </v-col>
          </v-row>
        </SectionCard>

        <SectionCard title="Clinical notes" icon="mdi-text-box-outline" class="mb-5">
          <v-textarea
            v-model="form.summary"
            label="Summary"
            rows="3"
          />
          <v-textarea
            v-model="form.findings"
            label="Findings (JSON)"
            rows="8"
            class="font-monospace"
            hint='Use a flexible object, for example {"risk_level":"moderate","observations":["Uses walker"]}.'
            persistent-hint
            :error-messages="errors.findings"
          />
          <v-textarea
            v-model="form.recommendations"
            label="Recommendations"
            rows="4"
          />
        </SectionCard>

        <div class="d-flex flex-wrap justify-end ga-3">
          <v-btn variant="text" :to="form.patient_id ? \`/patients/\${form.patient_id}\` : '/patients'">
            Cancel
          </v-btn>
          <v-btn color="primary" type="submit" :loading="saving" prepend-icon="mdi-content-save-outline">
            {{ isEdit ? 'Save changes' : 'Create assessment' }}
          </v-btn>
        </div>
      </v-form>
    </div>
  `,
};
