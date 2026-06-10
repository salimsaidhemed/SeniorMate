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
    backTo: {
      type: String,
      required: true,
    },
    documentLabel: {
      type: String,
      default: "SeniorMate",
    },
  },
  methods: {
    printReport() {
      window.print();
    },
  },
  template: `
    <div class="print-page">
      <div class="print-actions">
        <v-btn variant="text" prepend-icon="mdi-arrow-left" :to="backTo">
          Back
        </v-btn>
        <v-btn color="primary" prepend-icon="mdi-printer-outline" @click="printReport">
          Print / Save PDF
        </v-btn>
      </div>

      <article class="print-document">
        <header class="print-document__header">
          <div>
            <div class="print-document__brand">{{ documentLabel }}</div>
            <h1 class="print-document__title">{{ title }}</h1>
            <p v-if="subtitle" class="print-document__subtitle">{{ subtitle }}</p>
          </div>
          <div class="print-document__mark">
            <v-icon icon="mdi-heart-pulse" size="28" />
          </div>
        </header>

        <slot />

        <footer class="print-document__footer">
          Generated from SeniorMate
        </footer>
      </article>
    </div>
  `,
};
