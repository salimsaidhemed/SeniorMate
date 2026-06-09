export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      default: "",
    },
    icon: {
      type: String,
      default: "",
    },
  },
  template: `
    <v-card class="section-card">
      <div class="section-card__header">
        <v-icon v-if="icon" :icon="icon" color="primary" size="20" />
        <div>
          <div class="section-card__title">{{ title }}</div>
          <div v-if="subtitle" class="section-card__subtitle">{{ subtitle }}</div>
        </div>
      </div>
      <v-divider />
      <v-card-text>
        <slot />
      </v-card-text>
    </v-card>
  `,
};
