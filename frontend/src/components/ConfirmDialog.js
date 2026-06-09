export default {
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    message: {
      type: String,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    confirmLabel: {
      type: String,
      default: "Delete",
    },
  },
  emits: ["update:modelValue", "confirm"],
  template: `
    <v-dialog
      :model-value="modelValue"
      max-width="440"
      @update:model-value="$emit('update:modelValue', $event)"
    >
      <v-card>
        <v-card-title class="d-flex align-center ga-2">
          <v-icon icon="mdi-alert-outline" color="error" />
          {{ title }}
        </v-card-title>
        <v-card-text>{{ message }}</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="$emit('update:modelValue', false)">Cancel</v-btn>
          <v-btn color="error" variant="flat" :loading="loading" @click="$emit('confirm')">
            {{ confirmLabel }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  `,
};
