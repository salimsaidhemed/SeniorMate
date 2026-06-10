import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { createPatient, getPatient, updatePatient } from "../services/patients.js";

const emptyForm = {
  first_name: "",
  last_name: "",
  date_of_birth: "",
  gender: "",
  phone: "",
  email: "",
  address: "",
  emergency_contact_name: "",
  emergency_contact_phone: "",
  diagnosis_summary: "",
  status: "active",
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
    const errors = ref({});
    const error = ref("");
    const loading = ref(false);
    const saving = ref(false);

    const isEdit = computed(() => props.mode === "edit");
    const title = computed(() => (isEdit.value ? "Edit patient" : "New patient"));

    function validate() {
      const nextErrors = {};

      if (!form.value.first_name.trim()) {
        nextErrors.first_name = "First name is required.";
      }

      if (!form.value.last_name.trim()) {
        nextErrors.last_name = "Last name is required.";
      }

      errors.value = nextErrors;
      return Object.keys(nextErrors).length === 0;
    }

    function apiPayload() {
      const payload = {};

      for (const [key, value] of Object.entries(form.value)) {
        payload[key] = typeof value === "string" && value === "" ? null : value;
      }

      payload.first_name = form.value.first_name.trim();
      payload.last_name = form.value.last_name.trim();
      payload.status = form.value.status || "active";

      return payload;
    }

    async function loadPatient() {
      if (!isEdit.value) return;

      loading.value = true;
      error.value = "";

      try {
        const response = await getPatient(route.params.id);
        form.value = {
          ...emptyForm,
          ...response.data,
          date_of_birth: response.data.date_of_birth || "",
        };
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
          ? await updatePatient(route.params.id, apiPayload())
          : await createPatient(apiPayload());

        await router.push(`/patients/${response.data.id}`);
      } catch (err) {
        error.value = err.message;
        errors.value = err.payload?.errors || {};
      } finally {
        saving.value = false;
      }
    }

    onMounted(loadPatient);

    return {
      error,
      errors,
      form,
      isEdit,
      loading,
      saving,
      submit,
      title,
    };
  },
  template: `
    <div class="page-shell" style="max-width: 1040px;">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/patients" class="mb-4">
        Patients
      </v-btn>

      <h1 class="text-h4 font-weight-bold mb-5">{{ title }}</h1>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <v-form v-else @submit.prevent="submit">
        <v-card class="mb-5">
          <v-card-title>Demographics</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.first_name"
                  label="First name"
                  :error-messages="errors.first_name"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.last_name"
                  label="Last name"
                  :error-messages="errors.last_name"
                  required
                />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="form.date_of_birth" label="Date of birth" type="date" />
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="form.gender" label="Gender" />
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="form.status"
                  label="Status"
                  :items="['active', 'inactive']"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.phone" label="Phone" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.email" label="Email" type="email" />
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="form.address" label="Address" rows="2" />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card class="mb-5">
          <v-card-title>Emergency and clinical details</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.emergency_contact_name" label="Emergency contact name" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.emergency_contact_phone" label="Emergency contact phone" />
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="form.diagnosis_summary" label="Diagnosis summary" rows="3" />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <div class="d-flex justify-end ga-3">
          <v-btn variant="text" to="/patients">Cancel</v-btn>
          <v-btn color="primary" type="submit" :loading="saving">
            Save patient
          </v-btn>
        </div>
      </v-form>
    </div>
  `,
};
