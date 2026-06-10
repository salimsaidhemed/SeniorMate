export default {
  props: {
    type: {
      type: String,
      default: "table-row@5",
    },
  },
  template: `
    <div class="loading-state" aria-live="polite" aria-label="Loading content">
      <v-skeleton-loader :type="type" />
    </div>
  `,
};
