export default {
  props: {
    message: {
      type: String,
      default: "",
    },
  },
  template: `
    <v-alert
      v-if="message"
      type="error"
      variant="tonal"
      icon="mdi-alert-circle-outline"
      class="mb-5"
      role="alert"
    >
      {{ message }}
    </v-alert>
  `,
};
