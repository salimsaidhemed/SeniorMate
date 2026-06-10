import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import {
  DEFAULT_BRANDING,
  applyBranding,
  brandingState,
  defaultLogoUrl,
} from "../branding.js";
import {
  deleteBrandingLogo,
  getBranding,
  updateBranding,
  uploadBrandingLogo,
} from "../services/branding.js";


const HEX_COLOR = /^#[0-9A-Fa-f]{6}$/;

export default {
  setup() {
    const form = ref({ ...DEFAULT_BRANDING });
    const loading = ref(true);
    const saving = ref(false);
    const uploading = ref(false);
    const deleting = ref(false);
    const resetting = ref(false);
    const error = ref("");
    const success = ref("");
    const errors = ref({});
    const logoFile = ref(null);
    const logoPreview = ref("");
    const confirmDelete = ref(false);
    const confirmReset = ref(false);

    const previewLogo = computed(
      () => logoPreview.value || brandingState.logo_src || defaultLogoUrl,
    );

    function releasePreview() {
      if (logoPreview.value.startsWith("blob:")) {
        URL.revokeObjectURL(logoPreview.value);
      }
      logoPreview.value = "";
    }

    function selectedFile() {
      return Array.isArray(logoFile.value)
        ? logoFile.value[0]
        : logoFile.value;
    }

    function previewSelectedLogo() {
      releasePreview();
      const file = selectedFile();
      if (file) {
        logoPreview.value = URL.createObjectURL(file);
      }
    }

    function validate() {
      const nextErrors = {};
      for (const field of [
        "primary_color",
        "secondary_color",
        "accent_color",
        "sidebar_color",
      ]) {
        if (!HEX_COLOR.test(form.value[field] || "")) {
          nextErrors[field] = "Use a six-digit hex color.";
        }
      }
      errors.value = nextErrors;
      return Object.keys(nextErrors).length === 0;
    }

    function payload() {
      return {
        organization_name: form.value.organization_name || null,
        app_display_name: form.value.app_display_name || null,
        primary_color: form.value.primary_color,
        secondary_color: form.value.secondary_color,
        accent_color: form.value.accent_color,
        sidebar_color: form.value.sidebar_color,
        login_banner_text: form.value.login_banner_text || null,
        footer_text: form.value.footer_text || null,
      };
    }

    function syncForm(data) {
      form.value = {
        ...DEFAULT_BRANDING,
        ...data,
      };
      applyBranding(data);
    }

    async function loadBranding() {
      loading.value = true;
      error.value = "";
      try {
        const response = await getBranding();
        syncForm(response.data);
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    async function save() {
      error.value = "";
      success.value = "";
      if (!validate()) return;
      saving.value = true;
      try {
        const response = await updateBranding(payload());
        syncForm(response.data);
        success.value = "Branding settings saved.";
      } catch (err) {
        error.value = err.message;
        errors.value = err.payload?.errors || {};
      } finally {
        saving.value = false;
      }
    }

    async function uploadLogo() {
      const file = selectedFile();
      if (!file) {
        error.value = "Choose an SVG, PNG, or JPEG logo first.";
        return;
      }
      error.value = "";
      success.value = "";
      uploading.value = true;
      try {
        const response = await uploadBrandingLogo(file);
        releasePreview();
        logoFile.value = null;
        syncForm(response.data);
        success.value = "Organization logo updated.";
      } catch (err) {
        error.value = err.payload?.errors?.file || err.message;
      } finally {
        uploading.value = false;
      }
    }

    async function removeLogo() {
      deleting.value = true;
      error.value = "";
      try {
        const response = await deleteBrandingLogo();
        syncForm(response.data);
        success.value = "Default SeniorMate logo restored.";
        confirmDelete.value = false;
      } catch (err) {
        error.value = err.message;
      } finally {
        deleting.value = false;
      }
    }

    async function resetDefaults() {
      resetting.value = true;
      error.value = "";
      try {
        await deleteBrandingLogo();
        const response = await updateBranding({
          organization_name: null,
          app_display_name: null,
          primary_color: null,
          secondary_color: null,
          accent_color: null,
          sidebar_color: null,
          login_banner_text: null,
          footer_text: null,
        });
        syncForm(response.data);
        success.value = "SeniorMate default branding restored.";
        confirmReset.value = false;
      } catch (err) {
        error.value = err.message;
      } finally {
        resetting.value = false;
      }
    }

    onMounted(loadBranding);
    onBeforeUnmount(releasePreview);

    return {
      brandingState,
      confirmDelete,
      confirmReset,
      deleting,
      error,
      errors,
      form,
      loading,
      logoFile,
      previewLogo,
      previewSelectedLogo,
      removeLogo,
      resetDefaults,
      resetting,
      save,
      saving,
      success,
      uploadLogo,
      uploading,
    };
  },
  template: `
    <div class="page-shell">
      <PageHeader
        title="Branding"
        subtitle="Customize the organization identity used across SeniorMate."
        icon="mdi-palette-outline"
      >
        <template #actions>
          <v-btn
            variant="text"
            prepend-icon="mdi-restore"
            @click="confirmReset = true"
          >
            Reset defaults
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-content-save-outline"
            :loading="saving"
            @click="save"
          >
            Save branding
          </v-btn>
        </template>
      </PageHeader>

      <ErrorAlert :message="error" />
      <v-alert
        v-if="success"
        type="success"
        variant="tonal"
        class="mb-5"
        closable
        @click:close="success = ''"
      >
        {{ success }}
      </v-alert>

      <LoadingState v-if="loading" text="Loading branding settings..." />

      <v-row v-else>
        <v-col cols="12" lg="7">
          <v-form @submit.prevent="save">
            <SectionCard
              title="Organization identity"
              subtitle="Names and logo shown in the application shell."
              icon="mdi-domain"
              class="mb-5"
            >
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.app_display_name"
                    label="App display name"
                    placeholder="SeniorMate"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="form.organization_name"
                    label="Organization name"
                    placeholder="Organization name"
                  />
                </v-col>
                <v-col cols="12">
                  <v-file-input
                    v-model="logoFile"
                    label="Organization logo"
                    accept=".svg,.png,.jpg,.jpeg,image/svg+xml,image/png,image/jpeg"
                    prepend-icon="mdi-image-outline"
                    hint="SVG, PNG, or JPEG. Maximum 2 MB."
                    persistent-hint
                    @update:model-value="previewSelectedLogo"
                  />
                  <div class="d-flex ga-2 mt-3 flex-wrap">
                    <v-btn
                      color="primary"
                      variant="tonal"
                      prepend-icon="mdi-cloud-upload-outline"
                      :loading="uploading"
                      :disabled="!logoFile"
                      @click="uploadLogo"
                    >
                      Upload logo
                    </v-btn>
                    <v-btn
                      v-if="brandingState.has_custom_logo"
                      color="error"
                      variant="text"
                      prepend-icon="mdi-delete-outline"
                      @click="confirmDelete = true"
                    >
                      Delete custom logo
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </SectionCard>

            <SectionCard
              title="Theme colors"
              subtitle="Use accessible six-digit hex colors for the application shell."
              icon="mdi-format-color-fill"
              class="mb-5"
            >
              <v-row>
                <v-col
                  v-for="field in [
                    ['primary_color', 'Primary color'],
                    ['secondary_color', 'Secondary color'],
                    ['accent_color', 'Accent color'],
                    ['sidebar_color', 'Sidebar color'],
                  ]"
                  :key="field[0]"
                  cols="12"
                  sm="6"
                >
                  <div class="branding-color-field">
                    <input
                      v-model="form[field[0]]"
                      type="color"
                      :aria-label="field[1]"
                      class="branding-color-field__swatch"
                    />
                    <v-text-field
                      v-model="form[field[0]]"
                      :label="field[1]"
                      :error-messages="errors[field[0]]"
                    />
                  </div>
                </v-col>
              </v-row>
            </SectionCard>

            <SectionCard
              title="Supporting text"
              subtitle="Optional language for sign-in and application footer surfaces."
              icon="mdi-text-box-outline"
            >
              <v-textarea
                v-model="form.login_banner_text"
                label="Login banner text"
                rows="2"
                auto-grow
              />
              <v-textarea
                v-model="form.footer_text"
                label="Footer text"
                rows="2"
                auto-grow
              />
            </SectionCard>
          </v-form>
        </v-col>

        <v-col cols="12" lg="5">
          <div class="branding-preview-sticky">
            <h2 class="text-subtitle-1 font-weight-bold mb-3">Live preview</h2>
            <div
              class="branding-preview"
              :style="{ '--preview-sidebar': form.sidebar_color }"
            >
              <aside class="branding-preview__sidebar">
                <img
                  :src="previewLogo"
                  alt=""
                  class="branding-preview__logo"
                />
                <div class="branding-preview__app-name">
                  {{ form.app_display_name || 'SeniorMate' }}
                </div>
                <div class="branding-preview__org-name">
                  {{ form.organization_name || 'Care operations' }}
                </div>
                <div
                  class="branding-preview__nav-item branding-preview__nav-item--active"
                  :style="{ backgroundColor: form.primary_color }"
                >
                  Dashboard
                </div>
                <div class="branding-preview__nav-item">Patients</div>
                <div class="branding-preview__nav-item">Visits</div>
              </aside>
              <section class="branding-preview__content">
                <div class="branding-preview__heading">Care dashboard</div>
                <div class="branding-preview__metrics">
                  <div
                    class="branding-preview__metric"
                    :style="{ borderColor: form.primary_color }"
                  >
                    <strong>24</strong>
                    <span>Active patients</span>
                  </div>
                  <div
                    class="branding-preview__metric"
                    :style="{ borderColor: form.accent_color }"
                  >
                    <strong>8</strong>
                    <span>Visits today</span>
                  </div>
                </div>
                <div
                  v-if="form.login_banner_text"
                  class="branding-preview__banner"
                  :style="{ color: form.secondary_color }"
                >
                  {{ form.login_banner_text }}
                </div>
                <div class="branding-preview__footer">
                  {{ form.footer_text || 'SeniorMate care operations' }}
                </div>
              </section>
            </div>
          </div>
        </v-col>
      </v-row>

      <ConfirmDialog
        v-model="confirmDelete"
        title="Delete custom logo?"
        message="The application will immediately return to the default SeniorMate logo."
        confirm-label="Delete logo"
        :loading="deleting"
        @confirm="removeLogo"
      />
      <ConfirmDialog
        v-model="confirmReset"
        title="Reset all branding?"
        message="Names, colors, text, and the custom logo will return to SeniorMate defaults."
        confirm-label="Reset defaults"
        :loading="resetting"
        @confirm="resetDefaults"
      />
    </div>
  `,
};
