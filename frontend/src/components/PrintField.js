export default {
  props: {
    label: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number, Boolean],
      default: "",
    },
  },
  computed: {
    displayValue() {
      if (this.value === true) return "Yes";
      if (this.value === false) return "No";
      return this.value || "Not provided";
    },
  },
  template: `
    <div class="print-field">
      <div class="print-field__label">{{ label }}</div>
      <div class="print-field__value">{{ displayValue }}</div>
    </div>
  `,
};
