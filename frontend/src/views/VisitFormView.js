import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { listPatients } from "../services/patients.js";
import { createVisit, getVisit, updateVisit } from "../services/visits.js";

const emptyForm = {
  patient_id: null,
  visit_date: "",
  visit_type: "",
  staff_name: "",
  staff_role: "aide",
  time_in: "",
  time_out: "",
  status: "scheduled",
  notes: "",
};

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
    const form = ref({ ...emptyForm });
    const patients = ref([]);
    const errors = ref({});
    const error = ref("");
    const loading = ref(false);
    const saving = ref(false);

    const isEdit = computed(() => props.mode === "edit");
    const title = computed(() => (isEdit.value ? "Edit visit" : "New visit"));
    const patientOptions = computed(() =>
      patients.value.map((patient) => ({
        title: `${patient.first_name} ${patient.last_name}`,
        value: patient.id,
      }))
    );

    function validate() {
      const nextErrors = {};

      if (!form.value.patient_id) {
        nextErrors.patient_id = "Patient is required.";
      }

      if (!form.value.visit_date) {
        nextErrors.visit_date = "Visit date is required.";
      }

      if (!form.value.visit_type.trim()) {
        nextErrors.visit_type = "Visit type is required.";
      }

      errors.value = nextErrors;
      return Object.keys(nextErrors).length === 0;
    }

    function apiPayload() {
      const payload = {};

      for (const [key, value] of Object.entries(form.value)) {
        payload[key] = typeof value === "string" && value === "" ? null : value;
      }

      payload.patient_id = Number(form.value.patient_id);
      payload.visit_date = form.value.visit_date;
      payload.visit_type = form.value.visit_type.trim();
      payload.staff_role = form.value.staff_role || null;
      payload.status = form.value.status || "scheduled";

      return payload;
    }

    async function loadForm() {
      loading.value = true;
      error.value = "";

      try {
        const patientResponse = await listPatients();
        patients.value = patientResponse.data;

        if (isEdit.value) {
          const visitResponse = await getVisit(route.params.id);
          form.value = {
            ...emptyForm,
            ...visitResponse.data,
            visit_date: visitResponse.data.visit_date || "",
            time_in: visitResponse.data.time_in || "",
            time_out: visitResponse.data.time_out || "",
          };
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
          ? await updateVisit(route.params.id, apiPayload())
          : await createVisit(apiPayload());

        await router.push(`/visits/${response.data.id}`);
      } catch (err) {
        error.value = err.message;
        errors.value = err.payload?.errors || {};
      } finally {
        saving.value = false;
      }
    }

    onMounted(loadForm);

    return {
      error,
      errors,
      form,
      loading,
      patientOptions,
      saving,
      submit,
      title,
    };
  },
  template: `
    <v-container class="py-8" style="max-width: 960px;">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/visits" class="mb-4">
        Visits
      </v-btn>

      <h1 class="text-h4 font-weight-bold mb-5">{{ title }}</h1>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <v-form v-else @submit.prevent="submit">
        <v-card class="mb-5">
          <v-card-title>Visit details</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="form.patient_id"
                  label="Patient"
                  :items="patientOptions"
                  item-title="title"
                  item-value="value"
                  :error-messages="errors.patient_id"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.visit_date"
                  label="Visit date"
                  type="date"
                  :error-messages="errors.visit_date"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.visit_type"
                  label="Visit type"
                  :error-messages="errors.visit_type"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="form.status"
                  label="Status"
                  :items="['scheduled', 'completed', 'cancelled']"
                  :error-messages="errors.status"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card class="mb-5">
          <v-card-title>Staff and time</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.staff_name" label="Staff name" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="form.staff_role"
                  label="Staff role"
                  :items="['aide', 'nurse']"
                  :error-messages="errors.staff_role"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.time_in" label="Time in" type="time" :error-messages="errors.time_in" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.time_out" label="Time out" type="time" :error-messages="errors.time_out" />
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="form.notes" label="Notes" rows="4" />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <div class="d-flex justify-end ga-3">
          <v-btn variant="text" to="/visits">Cancel</v-btn>
          <v-btn color="primary" type="submit" :loading="saving">
            Save visit
          </v-btn>
        </div>
      </v-form>
    </v-container>
  `,
};
