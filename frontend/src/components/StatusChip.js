const colors = {
  active: "success",
  inactive: "grey",
  scheduled: "info",
  completed: "success",
  cancelled: "grey",
};

export default {
  props: {
    status: {
      type: String,
      default: "",
    },
  },
  computed: {
    chipColor() {
      return colors[this.status] || "primary";
    },
  },
  template: `
    <v-chip :color="chipColor" size="small" variant="tonal" class="text-capitalize">
      {{ status || 'Not set' }}
    </v-chip>
  `,
};
