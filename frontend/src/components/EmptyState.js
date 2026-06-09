export default {
  props: {
    icon: {
      type: String,
      default: "mdi-inbox-outline",
    },
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      default: "",
    },
    actionLabel: {
      type: String,
      default: "",
    },
    actionTo: {
      type: String,
      default: "",
    },
  },
  template: `
    <div class="empty-state">
      <div class="empty-state__icon">
        <v-icon :icon="icon" size="34" />
      </div>
      <div class="text-subtitle-1 font-weight-medium">{{ title }}</div>
      <div v-if="description" class="text-body-2 text-medium-emphasis mt-1">
        {{ description }}
      </div>
      <v-btn
        v-if="actionLabel"
        color="primary"
        variant="tonal"
        :to="actionTo"
        class="mt-4"
      >
        {{ actionLabel }}
      </v-btn>
    </div>
  `,
};
