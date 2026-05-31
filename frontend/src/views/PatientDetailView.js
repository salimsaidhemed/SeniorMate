import { computed, onMounted, ref } from "vue";

import { getPatient } from "../services/patients.js";

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const patient = ref(null);
    const loading = ref(true);
    const error = ref("");

    const fullName = computed(() =>
      patient.value ? `${patient.value.first_name} ${patient.value.last_name}` : ""
    );

    async function loadPatient() {
      loading.value = true;
      error.value = "";

      try {
        const response = await getPatient(props.id);
        patient.value = response.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadPatient);

    return {
      error,
      fullName,
      loading,
      patient,
    };
  },
  template: `
    <v-container class="py-8" style="max-width: 1120px;">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/patients" class="mb-4">
        Patients
      </v-btn>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <template v-else-if="patient">
        <v-row align="center" class="mb-5">
          <v-col cols="12" md="8">
            <h1 class="text-h4 font-weight-bold mb-2">{{ fullName }}</h1>
            <v-chip :color="patient.status === 'active' ? 'success' : 'grey'" size="small">
              {{ patient.status }}
            </v-chip>
          </v-col>
          <v-col cols="12" md="4" class="text-md-right">
            <v-btn color="primary" prepend-icon="mdi-pencil-outline" :to="\`/patients/\${patient.id}/edit\`">
              Edit patient
            </v-btn>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Demographics</v-card-title>
              <v-list>
                <v-list-item title="Date of birth" :subtitle="patient.date_of_birth || 'Not provided'" />
                <v-list-item title="Gender" :subtitle="patient.gender || 'Not provided'" />
                <v-list-item title="Phone" :subtitle="patient.phone || 'Not provided'" />
                <v-list-item title="Email" :subtitle="patient.email || 'Not provided'" />
                <v-list-item title="Address" :subtitle="patient.address || 'Not provided'" />
              </v-list>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card>
              <v-card-title>Emergency contact</v-card-title>
              <v-list>
                <v-list-item title="Name" :subtitle="patient.emergency_contact_name || 'Not provided'" />
                <v-list-item title="Phone" :subtitle="patient.emergency_contact_phone || 'Not provided'" />
              </v-list>
              <v-divider />
              <v-card-title>Diagnosis summary</v-card-title>
              <v-card-text>{{ patient.diagnosis_summary || 'Not provided' }}</v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-container>
  `,
};
