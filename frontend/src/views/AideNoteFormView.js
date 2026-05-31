import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { createAideNote, getAideNote, updateAideNote } from "../services/aideNotes.js";
import { getPatient, listPatients } from "../services/patients.js";
import { getVisit, listVisits } from "../services/visits.js";

const checklistSections = [
  {
    key: "personal_care",
    title: "Personal Care",
    items: ["Bath", "Oral care", "Hair care", "Skin care", "Dressing", "Toileting"],
  },
  {
    key: "nutrition",
    title: "Nutrition",
    items: ["Meal prepared", "Meal served", "Fluids offered", "Intake encouraged"],
  },
  {
    key: "mental_status",
    title: "Mental Status",
    items: ["Alert", "Oriented", "Confused", "Anxious", "Calm", "Forgetful"],
  },
  {
    key: "elimination",
    title: "Elimination",
    items: ["Voided", "Bowel movement", "Incontinent care", "Catheter care"],
  },
  {
    key: "activity",
    title: "Activity",
    items: ["Ambulated", "Transferred", "Range of motion", "Repositioned"],
  },
  {
    key: "assistive_devices",
    title: "Assistive Devices",
    items: ["Walker", "Cane", "Wheelchair", "Hospital bed", "Shower chair"],
  },
  {
    key: "housekeeping",
    title: "Housekeeping",
    items: ["Laundry", "Light cleaning", "Changed linens", "Trash removed"],
  },
];

const emptyForm = {
  patient_id: null,
  visit_id: null,
  additional_notes: "",
  aide_name: "",
  signature_data: "",
  signature_date: "",
  time_in: "",
  time_out: "",
  meal_percentage: null,
};

function emptyChecklist() {
  return Object.fromEntries(
    checklistSections.map((section) => [section.key, { completed: [] }])
  );
}

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
    const checklist = ref(emptyChecklist());
    const patients = ref([]);
    const visits = ref([]);
    const errors = ref({});
    const error = ref("");
    const loading = ref(false);
    const saving = ref(false);

    const isEdit = computed(() => props.mode === "edit");
    const title = computed(() => (isEdit.value ? "Edit aide note" : "New aide note"));
    const patientOptions = computed(() =>
      patients.value.map((patient) => ({
        title: `${patient.first_name} ${patient.last_name}`,
        value: patient.id,
      }))
    );
    const visitOptions = computed(() =>
      visits.value.map((visit) => ({
        title: `${visit.visit_date} · ${visit.visit_type}`,
        value: visit.id,
      }))
    );

    function normalizeChecklistValue(value) {
      return value && typeof value === "object" ? value : { completed: [] };
    }

    function validate() {
      const nextErrors = {};

      if (!form.value.patient_id) {
        nextErrors.patient_id = "Patient is required.";
      }

      if (!form.value.visit_id) {
        nextErrors.visit_id = "Visit is required.";
      }

      if (!form.value.aide_name.trim()) {
        nextErrors.aide_name = "Aide name is required.";
      }

      if (!form.value.time_in) {
        nextErrors.time_in = "Time in is required.";
      }

      if (!form.value.time_out) {
        nextErrors.time_out = "Time out is required.";
      }

      errors.value = nextErrors;
      return Object.keys(nextErrors).length === 0;
    }

    function apiPayload() {
      const payload = {
        patient_id: Number(form.value.patient_id),
        visit_id: Number(form.value.visit_id),
        additional_notes: form.value.additional_notes || null,
        aide_name: form.value.aide_name.trim(),
        signature_data: form.value.signature_data || null,
        signature_date: form.value.signature_date || null,
        time_in: form.value.time_in,
        time_out: form.value.time_out,
      };

      for (const section of checklistSections) {
        payload[section.key] = {
          ...checklist.value[section.key],
          completed: checklist.value[section.key].completed || [],
        };
      }

      payload.nutrition = {
        ...payload.nutrition,
        meal_percentage: form.value.meal_percentage
          ? Number(form.value.meal_percentage)
          : null,
      };

      return payload;
    }

    async function preloadFromVisit(visitId) {
      const visitResponse = await getVisit(visitId);
      const visit = visitResponse.data;
      form.value.patient_id = visit.patient_id;
      form.value.visit_id = visit.id;
      form.value.time_in = visit.time_in || "";
      form.value.time_out = visit.time_out || "";

      const patientResponse = await getPatient(visit.patient_id);
      patients.value = [patientResponse.data];
      visits.value = [visit];
    }

    async function loadForm() {
      loading.value = true;
      error.value = "";

      try {
        if (route.query.visit_id && !isEdit.value) {
          await preloadFromVisit(route.query.visit_id);
        } else {
          const [patientResponse, visitResponse] = await Promise.all([
            listPatients(),
            listVisits(),
          ]);
          patients.value = patientResponse.data;
          visits.value = visitResponse.data;
        }

        if (isEdit.value) {
          const noteResponse = await getAideNote(route.params.id);
          const note = noteResponse.data;
          form.value = {
            ...emptyForm,
            ...note,
            signature_date: note.signature_date || "",
            time_in: note.time_in || "",
            time_out: note.time_out || "",
            meal_percentage: note.nutrition?.meal_percentage || null,
          };
          checklist.value = emptyChecklist();

          for (const section of checklistSections) {
            checklist.value[section.key] = normalizeChecklistValue(note[section.key]);
          }
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
          ? await updateAideNote(route.params.id, apiPayload())
          : await createAideNote(apiPayload());

        await router.push(`/aide-notes/${response.data.id}`);
      } catch (err) {
        error.value = err.message;
        errors.value = err.payload?.errors || {};
      } finally {
        saving.value = false;
      }
    }

    onMounted(loadForm);

    return {
      checklist,
      checklistSections,
      error,
      errors,
      form,
      loading,
      patientOptions,
      saving,
      submit,
      title,
      visitOptions,
    };
  },
  template: `
    <v-container class="py-8" style="max-width: 1120px;">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/aide-notes" class="mb-4">
        Aide Notes
      </v-btn>

      <h1 class="text-h4 font-weight-bold mb-5">{{ title }}</h1>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <v-form v-else @submit.prevent="submit">
        <v-card class="mb-5">
          <v-card-title>Patient and visit</v-card-title>
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
                <v-select
                  v-model="form.visit_id"
                  label="Visit"
                  :items="visitOptions"
                  item-title="title"
                  item-value="value"
                  :error-messages="errors.visit_id"
                  required
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-row>
          <v-col
            v-for="section in checklistSections"
            :key="section.key"
            cols="12"
            md="6"
          >
            <v-card class="mb-5">
              <v-card-title>{{ section.title }}</v-card-title>
              <v-card-text>
                <v-checkbox
                  v-for="item in section.items"
                  :key="item"
                  v-model="checklist[section.key].completed"
                  :label="item"
                  :value="item"
                  density="compact"
                  hide-details
                />
                <v-text-field
                  v-if="section.key === 'nutrition'"
                  v-model="form.meal_percentage"
                  label="Meal percentage"
                  type="number"
                  min="0"
                  max="100"
                  class="mt-3"
                />
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card class="mb-5">
          <v-card-title>Additional Notes</v-card-title>
          <v-card-text>
            <v-textarea v-model="form.additional_notes" label="Notes / comments" rows="4" />
          </v-card-text>
        </v-card>

        <v-card class="mb-5">
          <v-card-title>Signature / Staff Details</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.aide_name"
                  label="Aide name"
                  :error-messages="errors.aide_name"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.signature_date" label="Signature date" type="date" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.time_in"
                  label="Time in"
                  type="time"
                  :error-messages="errors.time_in"
                  required
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.time_out"
                  label="Time out"
                  type="time"
                  :error-messages="errors.time_out"
                  required
                />
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="form.signature_data"
                  label="Signature data placeholder"
                  rows="2"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <div class="d-flex justify-end ga-3">
          <v-btn variant="text" to="/aide-notes">Cancel</v-btn>
          <v-btn color="primary" type="submit" :loading="saving">
            Save aide note
          </v-btn>
        </div>
      </v-form>
    </v-container>
  `,
};
