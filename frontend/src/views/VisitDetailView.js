import { computed, onMounted, ref } from "vue";

import { listPatients } from "../services/patients.js";
import { getVisit } from "../services/visits.js";

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const visit = ref(null);
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
        const [visitResponse, patientResponse] = await Promise.all([
          getVisit(props.id),
          listPatients(),
        ]);
        visit.value = visitResponse.data;
        patients.value = patientResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadVisit);

    return {
      error,
      loading,
      patient,
      patientName,
      visit,
    };
  },
  template: `
    <v-container class="py-8" style="max-width: 1120px;">
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
            <h1 class="text-h4 font-weight-bold mb-2">{{ visit.visit_type }}</h1>
            <div class="text-body-1 text-medium-emphasis mb-2">{{ visit.visit_date }} · {{ patientName }}</div>
            <v-chip :color="visit.status === 'completed' ? 'success' : visit.status === 'cancelled' ? 'grey' : 'primary'" size="small">
              {{ visit.status }}
            </v-chip>
          </v-col>
          <v-col cols="12" md="4" class="text-md-right">
            <v-btn color="primary" prepend-icon="mdi-pencil-outline" :to="\`/visits/\${visit.id}/edit\`">
              Edit visit
            </v-btn>
          </v-col>
        </v-row>

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
      </template>
    </v-container>
  `,
};
