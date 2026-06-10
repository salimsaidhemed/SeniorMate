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
  },
  template: `
    <section class="print-section">
      <div class="print-section__heading">
        <h2>{{ title }}</h2>
        <p v-if="subtitle">{{ subtitle }}</p>
      </div>
      <div class="print-section__body">
        <slot />
      </div>
    </section>
  `,
};
