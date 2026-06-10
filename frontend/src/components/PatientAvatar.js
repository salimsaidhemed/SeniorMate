import { computed, onBeforeUnmount, ref, watch } from "vue";

import { getPatientPhoto } from "../services/patients.js";


export default {
  props: {
    patient: {
      type: Object,
      required: true,
    },
    size: {
      type: [Number, String],
      default: 44,
    },
    showVerification: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const imageUrl = ref("");
    const loading = ref(false);

    const initials = computed(() => {
      const names = [props.patient.first_name, props.patient.last_name]
        .filter((name) => typeof name === "string" && name.trim())
        .map((name) => name.trim());

      if (!names.length) return "";
      if (names.length === 1) return names[0].charAt(0).toUpperCase();
      return `${names[0].charAt(0)}${names[1].charAt(0)}`.toUpperCase();
    });

    function clearImageUrl() {
      if (imageUrl.value) {
        URL.revokeObjectURL(imageUrl.value);
        imageUrl.value = "";
      }
    }

    async function loadPhoto() {
      clearImageUrl();
      if (!props.patient.has_photo) return;

      loading.value = true;
      try {
        const blob = await getPatientPhoto(props.patient.id);
        imageUrl.value = URL.createObjectURL(blob);
      } catch {
        imageUrl.value = "";
      } finally {
        loading.value = false;
      }
    }

    watch(
      () => [
        props.patient.id,
        props.patient.has_photo,
        props.patient.photo_uploaded_at,
      ],
      loadPhoto,
      { immediate: true }
    );
    onBeforeUnmount(clearImageUrl);

    return {
      imageUrl,
      initials,
      loading,
    };
  },
  template: `
    <div class="patient-avatar">
      <v-avatar :size="size" color="primary" class="patient-avatar__image">
        <v-img
          v-if="imageUrl"
          :src="imageUrl"
          :alt="\`\${patient.first_name || ''} \${patient.last_name || ''} profile photo\`"
          cover
        />
        <v-progress-circular v-else-if="loading" indeterminate size="20" width="2" />
        <span v-else-if="initials" class="font-weight-semibold">{{ initials }}</span>
        <v-icon v-else icon="mdi-account-outline" />
      </v-avatar>
      <v-tooltip
        v-if="showVerification && patient.has_photo"
        :text="patient.photo_verified ? 'Photo verified' : 'Photo not verified'"
      >
        <template #activator="{ props: tooltipProps }">
          <span
            v-bind="tooltipProps"
            class="patient-avatar__verification"
            :class="{ 'patient-avatar__verification--verified': patient.photo_verified }"
          >
            <v-icon
              :icon="patient.photo_verified ? 'mdi-check-decagram' : 'mdi-alert-circle'"
              size="16"
            />
          </span>
        </template>
      </v-tooltip>
    </div>
  `,
};
