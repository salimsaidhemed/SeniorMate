import { computed, onMounted, ref } from "vue";

import MedicalRecordsSection from "../components/MedicalRecordsSection.js";
import PatientAvatar from "../components/PatientAvatar.js";
import PatientAssessmentsSection from "../components/PatientAssessmentsSection.js";
import { getPatientAideNotes } from "../services/aideNotes.js";
import { getPatientNurseNotes } from "../services/nurseNotes.js";
import {
  deletePatientPhoto,
  getPatient,
  uploadPatientPhoto,
  verifyPatientPhoto,
} from "../services/patients.js";
import { deleteVisit, listPatientVisits } from "../services/visits.js";

export default {
  components: {
    MedicalRecordsSection,
    PatientAvatar,
    PatientAssessmentsSection,
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
    const aideNotes = ref([]);
    const nurseNotes = ref([]);
    const activeTab = ref("overview");
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const deleting = ref(false);
    const selectedVisit = ref(null);
    const confirmDelete = ref(false);
    const photoDialog = ref(false);
    const photoFile = ref(null);
    const uploadingPhoto = ref(false);
    const updatingVerification = ref(false);
    const deletingPhoto = ref(false);
    const confirmPhotoDelete = ref(false);

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
        const [
          patientResponse,
          visitResponse,
          aideNoteResponse,
          nurseNoteResponse,
        ] = await Promise.all([
          getPatient(props.id),
          listPatientVisits(props.id),
          getPatientAideNotes(props.id),
          getPatientNurseNotes(props.id),
        ]);
        patient.value = patientResponse.data;
        visits.value = visitResponse.data;
        aideNotes.value = aideNoteResponse.data;
        nurseNotes.value = nurseNoteResponse.data;
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

    function openPhotoDialog() {
      photoFile.value = null;
      photoDialog.value = true;
    }

    async function savePhoto() {
      const file = Array.isArray(photoFile.value)
        ? photoFile.value[0]
        : photoFile.value;
      if (!file) {
        error.value = "Choose a JPEG or PNG image.";
        return;
      }

      uploadingPhoto.value = true;
      error.value = "";
      success.value = "";
      try {
        const response = await uploadPatientPhoto(patient.value.id, file);
        patient.value = response.data;
        photoDialog.value = false;
        success.value = "Patient photo uploaded successfully.";
      } catch (err) {
        error.value = err.payload?.errors?.file || err.message;
      } finally {
        uploadingPhoto.value = false;
      }
    }

    async function togglePhotoVerification() {
      updatingVerification.value = true;
      error.value = "";
      success.value = "";
      try {
        const verified = !patient.value.photo_verified;
        const response = await verifyPatientPhoto(patient.value.id, verified);
        patient.value = response.data;
        success.value = verified
          ? "Patient photo marked verified."
          : "Patient photo marked unverified.";
      } catch (err) {
        error.value = err.message;
      } finally {
        updatingVerification.value = false;
      }
    }

    async function removePhoto() {
      deletingPhoto.value = true;
      error.value = "";
      success.value = "";
      try {
        const response = await deletePatientPhoto(patient.value.id);
        patient.value = response.data;
        confirmPhotoDelete.value = false;
        success.value = "Patient photo deleted successfully.";
      } catch (err) {
        error.value = err.message;
      } finally {
        deletingPhoto.value = false;
      }
    }

    onMounted(loadPatient);

    return {
      error,
      activeTab,
      aideNotes,
      askDelete,
      confirmDelete,
      confirmPhotoDelete,
      deleting,
      deletingPhoto,
      fullName,
      loading,
      nurseNotes,
      openPhotoDialog,
      patient,
      photoDialog,
      photoFile,
      removePhoto,
      removeVisit,
      savePhoto,
      selectedVisit,
      success,
      togglePhotoVerification,
      updatingVerification,
      uploadingPhoto,
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
        <DetailHeader
          eyebrow="Patient record"
          :title="fullName"
          :subtitle="patient.phone || patient.email || 'Contact information not provided'"
        >
          <template #avatar>
            <PatientAvatar :patient="patient" :size="84" show-verification />
          </template>
          <template #meta>
            <StatusChip :status="patient.status" />
            <v-chip
              v-if="patient.has_photo"
              :color="patient.photo_verified ? 'success' : 'warning'"
              size="small"
              variant="tonal"
              :prepend-icon="patient.photo_verified ? 'mdi-check-decagram' : 'mdi-alert-circle-outline'"
            >
              {{ patient.photo_verified ? 'Photo verified' : 'Photo review needed' }}
            </v-chip>
            <v-chip size="small" variant="outlined" prepend-icon="mdi-calendar-clock-outline">
              {{ visits.length }} {{ visits.length === 1 ? 'visit' : 'visits' }}
            </v-chip>
          </template>
          <template #actions>
              <v-btn color="primary" prepend-icon="mdi-calendar-plus-outline" :to="\`/visits/new?patient_id=\${patient.id}\`">
                New visit
              </v-btn>
              <v-btn color="primary" variant="tonal" prepend-icon="mdi-pencil-outline" :to="\`/patients/\${patient.id}/edit\`">
                Edit patient
              </v-btn>
              <v-btn variant="outlined" prepend-icon="mdi-printer-outline" :to="\`/patients/\${patient.id}/print\`">
                Print summary
              </v-btn>
              <v-btn variant="outlined" prepend-icon="mdi-camera-outline" @click="openPhotoDialog">
                {{ patient.has_photo ? 'Replace photo' : 'Upload photo' }}
              </v-btn>
              <v-btn
                v-if="patient.has_photo"
                variant="outlined"
                :prepend-icon="patient.photo_verified ? 'mdi-shield-off-outline' : 'mdi-check-decagram-outline'"
                :loading="updatingVerification"
                @click="togglePhotoVerification"
              >
                {{ patient.photo_verified ? 'Mark unverified' : 'Mark verified' }}
              </v-btn>
              <v-btn
                v-if="patient.has_photo"
                color="error"
                variant="text"
                prepend-icon="mdi-delete-outline"
                @click="confirmPhotoDelete = true"
              >
                Delete photo
              </v-btn>
          </template>
        </DetailHeader>

        <v-tabs v-model="activeTab" color="primary" class="record-tabs" show-arrows>
          <v-tab value="overview" prepend-icon="mdi-account-outline">Overview</v-tab>
          <v-tab value="visits" prepend-icon="mdi-calendar-clock-outline">Visits</v-tab>
          <v-tab value="records" prepend-icon="mdi-file-document-multiple-outline">Medical records</v-tab>
          <v-tab value="assessments" prepend-icon="mdi-clipboard-text-search-outline">Assessments</v-tab>
          <v-tab value="notes" prepend-icon="mdi-clipboard-pulse-outline">Care notes</v-tab>
        </v-tabs>

        <v-window v-model="activeTab">
          <v-window-item value="overview">
            <v-row class="detail-grid">
              <v-col cols="12" md="6">
                <SectionCard title="Demographics" icon="mdi-card-account-details-outline">
                  <v-list>
                    <v-list-item title="Date of birth" :subtitle="patient.date_of_birth || 'Not provided'" />
                    <v-list-item title="Gender" :subtitle="patient.gender || 'Not provided'" />
                    <v-list-item title="Phone" :subtitle="patient.phone || 'Not provided'" />
                    <v-list-item title="Email" :subtitle="patient.email || 'Not provided'" />
                    <v-list-item title="Address" :subtitle="patient.address || 'Not provided'" />
                  </v-list>
                </SectionCard>
              </v-col>

              <v-col cols="12" md="6">
                <SectionCard title="Care context" icon="mdi-heart-pulse">
                  <v-list>
                    <v-list-item title="Emergency contact" :subtitle="patient.emergency_contact_name || 'Not provided'" />
                    <v-list-item title="Emergency phone" :subtitle="patient.emergency_contact_phone || 'Not provided'" />
                  </v-list>
                  <v-divider class="my-3" />
                  <div class="text-subtitle-2 mb-2">Diagnosis summary</div>
                  <div class="text-body-2 text-medium-emphasis">
                    {{ patient.diagnosis_summary || 'Not provided' }}
                  </div>
                </SectionCard>
              </v-col>
            </v-row>
          </v-window-item>

          <v-window-item value="visits">
            <SectionCard
              title="Visits"
              subtitle="Scheduled and completed care for this patient."
              icon="mdi-calendar-clock-outline"
              class="data-card"
            >
              <div class="d-flex justify-end mb-4">
                <v-btn color="primary" prepend-icon="mdi-plus" :to="\`/visits/new?patient_id=\${patient.id}\`">
                  New visit
                </v-btn>
              </div>
              <v-data-table :headers="visitHeaders" :items="visits" item-value="id">
                <template #no-data>
                  <EmptyState
                    icon="mdi-calendar-plus-outline"
                    title="No visits yet"
                    description="Create the first visit for this patient."
                    action-label="Create visit"
                    :action-to="\`/visits/new?patient_id=\${patient.id}\`"
                  />
                </template>
                <template #[\`item.status\`]="{ item }">
                  <StatusChip :status="item.status" />
                </template>
                <template #[\`item.actions\`]="{ item }">
                  <div class="table-actions">
                    <v-btn icon="mdi-eye-outline" variant="text" :to="\`/visits/\${item.id}\`" aria-label="View visit" title="View visit" />
                    <v-btn icon="mdi-pencil-outline" variant="text" :to="\`/visits/\${item.id}/edit\`" aria-label="Edit visit" title="Edit visit" />
                    <v-btn icon="mdi-delete-outline" variant="text" color="error" aria-label="Delete visit" title="Delete visit" @click="askDelete(item)" />
                  </div>
                </template>
              </v-data-table>
            </SectionCard>
          </v-window-item>

          <v-window-item value="records">
            <MedicalRecordsSection :patient-id="patient.id" />
          </v-window-item>

          <v-window-item value="assessments">
            <PatientAssessmentsSection :patient-id="patient.id" />
          </v-window-item>

          <v-window-item value="notes">
            <v-row>
              <v-col cols="12" md="6">
                <SectionCard title="Aide notes" icon="mdi-clipboard-check-outline">
                  <EmptyState
                    v-if="!aideNotes.length"
                    icon="mdi-clipboard-text-outline"
                    title="No aide notes"
                    description="Aide notes linked to patient visits will appear here."
                  />
                  <v-list v-else lines="two">
                    <v-list-item
                      v-for="note in aideNotes"
                      :key="note.id"
                      :title="note.aide_name || 'Aide note'"
                      :subtitle="note.signature_date || 'Signature date not provided'"
                      :to="\`/aide-notes/\${note.id}\`"
                      append-icon="mdi-chevron-right"
                    />
                  </v-list>
                </SectionCard>
              </v-col>
              <v-col cols="12" md="6">
                <SectionCard title="Nurse notes" icon="mdi-clipboard-pulse-outline">
                  <EmptyState
                    v-if="!nurseNotes.length"
                    icon="mdi-clipboard-text-outline"
                    title="No nurse notes"
                    description="Nurse notes linked to patient visits will appear here."
                  />
                  <v-list v-else lines="two">
                    <v-list-item
                      v-for="note in nurseNotes"
                      :key="note.id"
                      :title="note.diagnosis || 'Nurse note'"
                      :subtitle="note.signature_date || 'Signature date not provided'"
                      :to="\`/nurse-notes/\${note.id}\`"
                      append-icon="mdi-chevron-right"
                    />
                  </v-list>
                </SectionCard>
              </v-col>
            </v-row>
          </v-window-item>
        </v-window>
      </template>

      <v-dialog v-model="photoDialog" max-width="560">
        <v-card>
          <v-card-title class="d-flex align-center ga-2">
            <v-icon icon="mdi-camera-outline" color="primary" />
            {{ patient?.has_photo ? 'Replace patient photo' : 'Upload patient photo' }}
          </v-card-title>
          <v-card-text>
            <v-file-input
              v-model="photoFile"
              label="Patient photo *"
              accept=".jpg,.jpeg,.png"
              prepend-icon="mdi-image-outline"
              show-size
              hint="JPEG or PNG. Maximum 5 MB. New photos start unverified."
              persistent-hint
            />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="photoDialog = false">Cancel</v-btn>
            <v-btn color="primary" :loading="uploadingPhoto" @click="savePhoto">
              {{ patient?.has_photo ? 'Replace photo' : 'Upload photo' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <ConfirmDialog
        v-model="confirmPhotoDelete"
        title="Delete patient photo"
        message="Delete this patient profile photo? The private stored image will also be removed."
        :loading="deletingPhoto"
        @confirm="removePhoto"
      />

      <ConfirmDialog
        v-model="confirmDelete"
        title="Delete visit"
        :message="\`Delete \${selectedVisit?.visit_type || 'this visit'} from \${selectedVisit?.visit_date || 'the patient record'}?\`"
        :loading="deleting"
        @confirm="removeVisit"
      />
    </div>
  `,
};
