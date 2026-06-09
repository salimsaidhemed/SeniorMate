import { onMounted, ref } from "vue";

import {
  deleteMedicalRecord,
  downloadMedicalRecord,
  getPatientMedicalRecords,
  updateMedicalRecord,
  uploadMedicalRecord,
} from "../services/medicalRecords.js";


const emptyUploadForm = () => ({
  title: "",
  description: "",
  record_type: "",
  uploaded_by: "",
  file: null,
});

const emptyEditForm = () => ({
  title: "",
  description: "",
  record_type: "",
  uploaded_by: "",
});

export default {
  props: {
    patientId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const records = ref([]);
    const loading = ref(true);
    const error = ref("");
    const success = ref("");
    const uploadDialog = ref(false);
    const editDialog = ref(false);
    const confirmDelete = ref(false);
    const uploading = ref(false);
    const saving = ref(false);
    const deleting = ref(false);
    const downloadingId = ref(null);
    const selectedRecord = ref(null);
    const uploadForm = ref(emptyUploadForm());
    const editForm = ref(emptyEditForm());

    const headers = [
      { title: "Title", key: "title" },
      { title: "Type", key: "record_type" },
      { title: "File", key: "file_name" },
      { title: "Size", key: "file_size" },
      { title: "Uploaded", key: "uploaded_at" },
      { title: "Actions", key: "actions", sortable: false },
    ];

    const recordTypes = [
      { title: "Assessment", value: "assessment" },
      { title: "Care plan", value: "care_plan" },
      { title: "Prescription", value: "prescription" },
      { title: "Lab result", value: "lab_result" },
      { title: "Scan", value: "scan" },
      { title: "Other", value: "other" },
    ];

    async function loadRecords() {
      loading.value = true;
      error.value = "";
      try {
        const response = await getPatientMedicalRecords(props.patientId);
        records.value = response.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function openUpload() {
      uploadForm.value = emptyUploadForm();
      error.value = "";
      uploadDialog.value = true;
    }

    function selectedFile() {
      const value = uploadForm.value.file;
      return Array.isArray(value) ? value[0] : value;
    }

    async function submitUpload() {
      const file = selectedFile();
      if (!uploadForm.value.title.trim() || !file) {
        error.value = "Title and file are required.";
        return;
      }

      uploading.value = true;
      error.value = "";
      success.value = "";
      try {
        await uploadMedicalRecord({
          ...uploadForm.value,
          patient_id: props.patientId,
          title: uploadForm.value.title.trim(),
          file,
        });
        uploadDialog.value = false;
        success.value = "Medical record uploaded successfully.";
        await loadRecords();
      } catch (err) {
        error.value = err.payload?.errors?.file || err.message;
      } finally {
        uploading.value = false;
      }
    }

    function openEdit(record) {
      selectedRecord.value = record;
      editForm.value = {
        title: record.title || "",
        description: record.description || "",
        record_type: record.record_type || "",
        uploaded_by: record.uploaded_by || "",
      };
      error.value = "";
      editDialog.value = true;
    }

    async function saveMetadata() {
      if (!editForm.value.title.trim()) {
        error.value = "Title is required.";
        return;
      }

      saving.value = true;
      error.value = "";
      success.value = "";
      try {
        await updateMedicalRecord(selectedRecord.value.id, {
          ...editForm.value,
          title: editForm.value.title.trim(),
        });
        editDialog.value = false;
        success.value = "Medical record details updated.";
        await loadRecords();
      } catch (err) {
        error.value = err.message;
      } finally {
        saving.value = false;
      }
    }

    function askDelete(record) {
      selectedRecord.value = record;
      confirmDelete.value = true;
    }

    async function removeRecord() {
      if (!selectedRecord.value) return;

      deleting.value = true;
      error.value = "";
      success.value = "";
      try {
        await deleteMedicalRecord(selectedRecord.value.id);
        confirmDelete.value = false;
        success.value = "Medical record deleted successfully.";
        selectedRecord.value = null;
        await loadRecords();
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    async function downloadRecord(record) {
      downloadingId.value = record.id;
      error.value = "";
      try {
        const blob = await downloadMedicalRecord(record.id);
        const url = URL.createObjectURL(blob);
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = record.file_name;
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
        URL.revokeObjectURL(url);
      } catch (err) {
        error.value = err.message;
      } finally {
        downloadingId.value = null;
      }
    }

    function formatBytes(bytes) {
      if (!bytes) return "0 B";
      if (bytes < 1024 * 1024) return `${Math.ceil(bytes / 1024)} KB`;
      return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }

    function formatDate(value) {
      if (!value) return "Not available";
      return new Intl.DateTimeFormat(undefined, {
        dateStyle: "medium",
      }).format(new Date(value));
    }

    onMounted(loadRecords);

    return {
      askDelete,
      confirmDelete,
      deleting,
      downloadRecord,
      downloadingId,
      editDialog,
      editForm,
      error,
      formatBytes,
      formatDate,
      headers,
      loading,
      openEdit,
      openUpload,
      recordTypes,
      records,
      removeRecord,
      saveMetadata,
      saving,
      selectedRecord,
      submitUpload,
      success,
      uploadDialog,
      uploadForm,
      uploading,
    };
  },
  template: `
    <SectionCard
      title="Medical Records"
      subtitle="Private patient documents stored securely in MinIO."
      icon="mdi-file-document-multiple-outline"
      class="data-card mb-6"
    >
      <template #default>
        <div class="d-flex flex-wrap justify-space-between align-center ga-3 mb-4">
          <div class="text-body-2 text-medium-emphasis">
            PDFs, images, Word documents, care plans, prescriptions, and assessments.
          </div>
          <v-btn color="primary" prepend-icon="mdi-upload-outline" @click="openUpload">
            Upload record
          </v-btn>
        </div>

        <ErrorAlert :message="error" />
        <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
          {{ success }}
        </v-alert>

        <v-data-table
          :headers="headers"
          :items="records"
          :loading="loading"
          item-value="id"
          density="comfortable"
        >
          <template #loading>
            <LoadingState />
          </template>

          <template #no-data>
            <EmptyState
              icon="mdi-file-document-plus-outline"
              title="No medical records"
              description="Upload the first clinical document for this patient."
            />
          </template>

          <template #[\`item.record_type\`]="{ item }">
            {{ item.record_type?.replaceAll('_', ' ') || 'Other' }}
          </template>

          <template #[\`item.file_name\`]="{ item }">
            <div>
              <div class="font-weight-medium">{{ item.file_name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.file_mime_type }}</div>
            </div>
          </template>

          <template #[\`item.file_size\`]="{ item }">
            {{ formatBytes(item.file_size) }}
          </template>

          <template #[\`item.uploaded_at\`]="{ item }">
            <div>{{ formatDate(item.uploaded_at) }}</div>
            <div v-if="item.uploaded_by" class="text-caption text-medium-emphasis">
              {{ item.uploaded_by }}
            </div>
          </template>

          <template #[\`item.actions\`]="{ item }">
            <div class="table-actions">
              <v-btn
                icon="mdi-download-outline"
                variant="text"
                color="primary"
                :loading="downloadingId === item.id"
                aria-label="Download medical record"
                @click="downloadRecord(item)"
              />
              <v-btn
                icon="mdi-pencil-outline"
                variant="text"
                aria-label="Edit medical record details"
                @click="openEdit(item)"
              />
              <v-btn
                icon="mdi-delete-outline"
                variant="text"
                color="error"
                aria-label="Delete medical record"
                @click="askDelete(item)"
              />
            </div>
          </template>
        </v-data-table>
      </template>
    </SectionCard>

    <v-dialog v-model="uploadDialog" max-width="680">
      <v-card>
        <v-card-title class="d-flex align-center ga-2">
          <v-icon icon="mdi-upload-outline" color="primary" />
          Upload medical record
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submitUpload">
            <v-row>
              <v-col cols="12" md="7">
                <v-text-field v-model="uploadForm.title" label="Title *" />
              </v-col>
              <v-col cols="12" md="5">
                <v-select
                  v-model="uploadForm.record_type"
                  :items="recordTypes"
                  label="Record type"
                  clearable
                />
              </v-col>
              <v-col cols="12">
                <v-file-input
                  v-model="uploadForm.file"
                  label="Document *"
                  accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                  prepend-icon="mdi-paperclip"
                  show-size
                  hint="PDF, JPEG, PNG, DOC, or DOCX. Maximum 10 MB."
                  persistent-hint
                />
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="uploadForm.description"
                  label="Description"
                  rows="3"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="uploadForm.uploaded_by" label="Uploaded by" />
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="uploadDialog = false">Cancel</v-btn>
          <v-btn color="primary" :loading="uploading" @click="submitUpload">
            Upload record
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="editDialog" max-width="640">
      <v-card>
        <v-card-title class="d-flex align-center ga-2">
          <v-icon icon="mdi-file-edit-outline" color="primary" />
          Edit medical record
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="7">
              <v-text-field v-model="editForm.title" label="Title *" />
            </v-col>
            <v-col cols="12" md="5">
              <v-select
                v-model="editForm.record_type"
                :items="recordTypes"
                label="Record type"
                clearable
              />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="editForm.description" label="Description" rows="3" />
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="editForm.uploaded_by" label="Uploaded by" />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="editDialog = false">Cancel</v-btn>
          <v-btn color="primary" :loading="saving" @click="saveMetadata">
            Save changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <ConfirmDialog
      v-model="confirmDelete"
      title="Delete medical record"
      :message="\`Delete \${selectedRecord?.title || 'this medical record'} and its stored file? This cannot be undone.\`"
      :loading="deleting"
      @confirm="removeRecord"
    />
  `,
};
