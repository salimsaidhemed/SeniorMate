import { computed, onMounted, ref } from "vue";

import MedicalRecordsSection from "../components/MedicalRecordsSection.js";
import { getPatient } from "../services/patients.js";
import { deleteVisit, listPatientVisits } from "../services/visits.js";

export default {
  components: {
    MedicalRecordsSection,
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const patient = ref(null);
    const visits = ref([]);
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const deleting = ref(false);
    const selectedVisit = ref(null);
    const confirmDelete = ref(false);

    const visitHeaders = [
      { title: "Visit date", key: "visit_date" },
      { title: "Visit type", key: "visit_type" },
      { title: "Staff name", key: "staff_name" },
      { title: "Staff role", key: "staff_role" },
      { title: "Status", key: "status" },
      { title: "Actions", key: "actions", sortable: false },
    ];

    const fullName = computed(() =>
      patient.value ? `${patient.value.first_name} ${patient.value.last_name}` : ""
    );

    async function loadPatient() {
      loading.value = true;
      error.value = "";

      try {
        const [patientResponse, visitResponse] = await Promise.all([
          getPatient(props.id),
          listPatientVisits(props.id),
        ]);
        patient.value = patientResponse.data;
        visits.value = visitResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function askDelete(visit) {
      selectedVisit.value = visit;
      confirmDelete.value = true;
    }

    async function removeVisit() {
      if (!selectedVisit.value) return;

      deleting.value = true;
      error.value = "";
      success.value = "";

      try {
        await deleteVisit(selectedVisit.value.id);
        success.value = "Visit deleted successfully.";
        confirmDelete.value = false;
        selectedVisit.value = null;
        await loadPatient();
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    onMounted(loadPatient);

    return {
      error,
      askDelete,
      confirmDelete,
      deleting,
      fullName,
      loading,
      patient,
      removeVisit,
      selectedVisit,
      success,
      visitHeaders,
      visits,
    };
  },
  template: `
    <div class="page-shell">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/patients" class="mb-4">
        Patients
      </v-btn>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>
      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        {{ success }}
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
            <v-btn color="primary" prepend-icon="mdi-calendar-plus-outline" :to="\`/visits/new?patient_id=\${patient.id}\`" class="mr-2">
              New visit
            </v-btn>
            <v-btn color="primary" variant="tonal" prepend-icon="mdi-pencil-outline" :to="\`/patients/\${patient.id}/edit\`">
              Edit patient
            </v-btn>
          </v-col>
        </v-row>

        <v-row class="mb-5">
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

        <MedicalRecordsSection :patient-id="patient.id" />

        <v-card>
          <v-card-title>Visits</v-card-title>
          <v-data-table
            :headers="visitHeaders"
            :items="visits"
            item-value="id"
          >
            <template #no-data>
              <div class="pa-8 text-center">
                <v-icon icon="mdi-calendar-clock-outline" size="40" class="mb-3" />
                <div class="text-h6 mb-2">No visits yet</div>
                <v-btn color="primary" variant="flat" :to="\`/visits/new?patient_id=\${patient.id}\`">Create visit</v-btn>
              </div>
            </template>

            <template #[\`item.status\`]="{ item }">
              <v-chip :color="item.status === 'completed' ? 'success' : item.status === 'cancelled' ? 'grey' : 'primary'" size="small">
                {{ item.status }}
              </v-chip>
            </template>

            <template #[\`item.actions\`]="{ item }">
              <v-btn icon="mdi-eye-outline" variant="text" :to="\`/visits/\${item.id}\`" aria-label="View visit" />
              <v-btn icon="mdi-pencil-outline" variant="text" :to="\`/visits/\${item.id}/edit\`" aria-label="Edit visit" />
              <v-btn icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete visit" @click="askDelete(item)" />
            </template>
          </v-data-table>
        </v-card>
      </template>

      <v-dialog v-model="confirmDelete" max-width="440">
        <v-card>
          <v-card-title>Delete visit</v-card-title>
          <v-card-text>
            Delete {{ selectedVisit?.visit_type }} from {{ selectedVisit?.visit_date }}?
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="confirmDelete = false">Cancel</v-btn>
            <v-btn color="error" variant="flat" :loading="deleting" @click="removeVisit">
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  `,
};
