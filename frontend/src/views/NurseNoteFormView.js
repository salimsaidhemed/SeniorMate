import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { createNurseNote, getNurseNote, updateNurseNote } from "../services/nurseNotes.js";
import { getPatient, listPatients } from "../services/patients.js";
import { getVisit, listVisits } from "../services/visits.js";

const clinicalSections = [
  {
    key: "living_arrangements",
    title: "Patient / Visit Info",
    fields: [
      { key: "arrangement", label: "Living arrangement" },
      { key: "caregiver", label: "Primary caregiver" },
    ],
  },
  {
    key: "visit_type",
    title: "Visit Type",
    fields: [
      { key: "type", label: "Visit type" },
      { key: "purpose", label: "Visit purpose" },
    ],
  },
  {
    key: "vital_signs",
    title: "Vital Signs",
    fields: [
      { key: "blood_pressure", label: "Blood pressure" },
      { key: "pulse", label: "Pulse" },
      { key: "respirations", label: "Respirations" },
      { key: "temperature", label: "Temperature" },
      { key: "oxygen_saturation", label: "Oxygen saturation" },
      { key: "weight", label: "Weight" },
    ],
  },
  {
    key: "diet",
    title: "Diet",
    fields: [
      { key: "ordered", label: "Ordered diet" },
      { key: "appetite", label: "Appetite" },
      { key: "restrictions", label: "Restrictions" },
    ],
  },
  {
    key: "pain_assessment",
    title: "Pain Assessment",
    fields: [
      { key: "pain_level", label: "Pain level" },
      { key: "location", label: "Location" },
      { key: "intervention", label: "Intervention" },
      { key: "response", label: "Response" },
    ],
  },
  {
    key: "sensory",
    title: "Sensory",
    fields: [
      { key: "vision", label: "Vision" },
      { key: "hearing", label: "Hearing" },
      { key: "speech", label: "Speech" },
    ],
  },
  {
    key: "neuro",
    title: "Neuro",
    fields: [
      { key: "orientation", label: "Orientation" },
      { key: "pupils", label: "Pupils" },
      { key: "weakness", label: "Weakness" },
    ],
  },
  {
    key: "respiratory",
    title: "Respiratory",
    fields: [
      { key: "lung_sounds", label: "Lung sounds" },
      { key: "cough", label: "Cough" },
      { key: "oxygen_use", label: "Oxygen use" },
    ],
  },
  {
    key: "cardiac",
    title: "Cardiac",
    fields: [
      { key: "rhythm", label: "Rhythm" },
      { key: "chest_pain", label: "Chest pain" },
      { key: "education", label: "Education" },
    ],
  },
  {
    key: "peripheral_circulation",
    title: "Peripheral / Circulation",
    fields: [
      { key: "edema", label: "Edema" },
      { key: "pedal_pulses", label: "Pedal pulses" },
      { key: "capillary_refill", label: "Capillary refill" },
    ],
  },
  {
    key: "genitourinary",
    title: "Genitourinary",
    fields: [
      { key: "voiding", label: "Voiding" },
      { key: "urine", label: "Urine" },
      { key: "catheter", label: "Catheter" },
    ],
  },
  {
    key: "gastrointestinal",
    title: "Gastrointestinal",
    fields: [
      { key: "bowel_sounds", label: "Bowel sounds" },
      { key: "last_bowel_movement", label: "Last bowel movement" },
      { key: "nausea_vomiting", label: "Nausea / vomiting" },
    ],
  },
  {
    key: "endocrine",
    title: "Endocrine",
    fields: [
      { key: "blood_glucose", label: "Blood glucose" },
      { key: "insulin", label: "Insulin" },
      { key: "teaching", label: "Teaching" },
    ],
  },
  {
    key: "skin_integrity",
    title: "Skin Integrity",
    fields: [
      { key: "integrity", label: "Skin integrity" },
      { key: "color", label: "Color" },
      { key: "turgor", label: "Turgor" },
    ],
  },
  {
    key: "wound_evaluation",
    title: "Wound Evaluation",
    fields: [
      { key: "location", label: "Location" },
      { key: "appearance", label: "Appearance" },
      { key: "drainage", label: "Drainage" },
      { key: "treatment", label: "Treatment" },
    ],
  },
  {
    key: "mental_status",
    title: "Mental Status",
    fields: [
      { key: "mood", label: "Mood" },
      { key: "affect", label: "Affect" },
      { key: "safety", label: "Safety concerns" },
    ],
  },
  {
    key: "functional_status",
    title: "Functional Status",
    fields: [
      { key: "ambulation", label: "Ambulation" },
      { key: "transfers", label: "Transfers" },
      { key: "assistive_devices", label: "Assistive devices" },
    ],
  },
  {
    key: "homebound_status",
    title: "Homebound Status",
    fields: [
      { key: "reason", label: "Homebound reason" },
      { key: "taxing_effort", label: "Taxing effort" },
    ],
  },
  {
    key: "patient_caregiver_understanding",
    title: "Patient / Caregiver Understanding",
    fields: [
      { key: "understanding", label: "Understanding" },
      { key: "teaching_provided", label: "Teaching provided" },
    ],
  },
  {
    key: "md_contact",
    title: "MD Contact",
    fields: [
      { key: "contacted", label: "Contacted" },
      { key: "reason", label: "Reason" },
      { key: "outcome", label: "Outcome" },
    ],
  },
];

const textSections = [
  { key: "skilled_nursing", title: "Skilled Nursing" },
  { key: "response_to_intervention", title: "Response to Intervention" },
  { key: "discharge_planning", title: "Discharge Planning" },
  { key: "patient_feedback", title: "Patient / Family Feedback" },
  { key: "narrative", title: "Narrative" },
];

const emptyForm = {
  patient_id: null,
  visit_id: null,
  diagnosis: "",
  skilled_nursing: "",
  response_to_intervention: "",
  discharge_planning: "",
  patient_feedback: "",
  narrative: "",
  signature_data: "",
  signature_date: "",
};

function emptyClinicalSections() {
  return Object.fromEntries(
    clinicalSections.map((section) => [section.key, {}])
  );
}

function cleanSection(section) {
  return Object.fromEntries(
    Object.entries(section || {}).filter(([, value]) => value !== "" && value !== null)
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
    const clinical = ref(emptyClinicalSections());
    const patients = ref([]);
    const visits = ref([]);
    const errors = ref({});
    const error = ref("");
    const loading = ref(false);
    const saving = ref(false);

    const isEdit = computed(() => props.mode === "edit");
    const title = computed(() => (isEdit.value ? "Edit nurse note" : "New nurse note"));
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

    function validate() {
      const nextErrors = {};

      if (!form.value.patient_id) {
        nextErrors.patient_id = "Patient is required.";
      }

      if (!form.value.visit_id) {
        nextErrors.visit_id = "Visit is required.";
      }

      errors.value = nextErrors;
      return Object.keys(nextErrors).length === 0;
    }

    function apiPayload() {
      const payload = {
        patient_id: Number(form.value.patient_id),
        visit_id: Number(form.value.visit_id),
        diagnosis: form.value.diagnosis.trim() || null,
        signature_data: form.value.signature_data.trim() || null,
        signature_date: form.value.signature_date || null,
      };

      for (const section of clinicalSections) {
        payload[section.key] = cleanSection(clinical.value[section.key]);
      }

      for (const section of textSections) {
        payload[section.key] = form.value[section.key].trim() || null;
      }

      return payload;
    }

    async function preloadFromVisit(visitId) {
      const visitResponse = await getVisit(visitId);
      const visit = visitResponse.data;
      form.value.patient_id = visit.patient_id;
      form.value.visit_id = visit.id;
      clinical.value.visit_type = {
        ...clinical.value.visit_type,
        type: visit.visit_type || "",
      };

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
          const noteResponse = await getNurseNote(route.params.id);
          const note = noteResponse.data;
          form.value = {
            ...emptyForm,
            ...note,
            diagnosis: note.diagnosis || "",
            skilled_nursing: note.skilled_nursing || "",
            response_to_intervention: note.response_to_intervention || "",
            discharge_planning: note.discharge_planning || "",
            patient_feedback: note.patient_feedback || "",
            narrative: note.narrative || "",
            signature_data: note.signature_data || "",
            signature_date: note.signature_date || "",
          };
          clinical.value = emptyClinicalSections();

          for (const section of clinicalSections) {
            clinical.value[section.key] =
              note[section.key] && typeof note[section.key] === "object"
                ? note[section.key]
                : {};
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
          ? await updateNurseNote(route.params.id, apiPayload())
          : await createNurseNote(apiPayload());

        await router.push(`/nurse-notes/${response.data.id}`);
      } catch (err) {
        error.value = err.message;
        errors.value = err.payload?.errors || {};
      } finally {
        saving.value = false;
      }
    }

    onMounted(loadForm);

    return {
      clinical,
      clinicalSections,
      error,
      errors,
      form,
      loading,
      patientOptions,
      saving,
      submit,
      textSections,
      title,
      visitOptions,
    };
  },
  template: `
    <div class="page-shell">
      <v-btn variant="text" prepend-icon="mdi-arrow-left" to="/nurse-notes" class="mb-4">
        Nurse Notes
      </v-btn>

      <h1 class="text-h4 font-weight-bold mb-5">{{ title }}</h1>

      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
        {{ error }}
      </v-alert>

      <v-skeleton-loader v-if="loading" type="heading, paragraph, card" />

      <v-form v-else @submit.prevent="submit">
        <v-card class="mb-5">
          <v-card-title>Patient / Visit Info</v-card-title>
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
              <v-col cols="12">
                <v-textarea v-model="form.diagnosis" label="Diagnosis" rows="2" />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-row>
          <v-col
            v-for="section in clinicalSections"
            :key="section.key"
            cols="12"
            md="6"
          >
            <v-card class="mb-5">
              <v-card-title>{{ section.title }}</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col v-for="field in section.fields" :key="field.key" cols="12" md="6">
                    <v-text-field
                      v-model="clinical[section.key][field.key]"
                      :label="field.label"
                      density="comfortable"
                    />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-for="section in textSections" :key="section.key" class="mb-5">
          <v-card-title>{{ section.title }}</v-card-title>
          <v-card-text>
            <v-textarea v-model="form[section.key]" :label="section.title" rows="4" />
          </v-card-text>
        </v-card>

        <v-card class="mb-5">
          <v-card-title>Signature</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.signature_date" label="Signature date" type="date" />
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
          <v-btn variant="text" to="/nurse-notes">Cancel</v-btn>
          <v-btn color="primary" type="submit" :loading="saving">
            Save nurse note
          </v-btn>
        </div>
      </v-form>
    </div>
  `,
};
