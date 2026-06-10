function titleize(value) {
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatValue(value) {
  if (Array.isArray(value)) {
    return value.map((item) => formatValue(item)).join(", ");
  }
  if (value && typeof value === "object") {
    return Object.entries(value)
      .map(([key, item]) => `${titleize(key)}: ${formatValue(item)}`)
      .join("; ");
  }
  if (value === true) return "Yes";
  if (value === false) return "No";
  return value === null || value === undefined || value === ""
    ? "Not documented"
    : String(value);
}

export default {
  props: {
    data: {
      type: [Object, Array],
      default: null,
    },
    emptyText: {
      type: String,
      default: "Not documented",
    },
  },
  computed: {
    entries() {
      if (!this.data) return [];
      if (Array.isArray(this.data)) {
        return this.data.map((value, index) => ({
          label: `Item ${index + 1}`,
          value: formatValue(value),
        }));
      }
      return Object.entries(this.data)
        .filter(([, value]) => value !== null && value !== "" && value !== undefined)
        .map(([key, value]) => ({
          label: titleize(key),
          value: formatValue(value),
        }));
    },
  },
  template: `
    <div v-if="entries.length" class="checklist-summary">
      <div v-for="entry in entries" :key="entry.label" class="checklist-summary__item">
        <span class="checklist-summary__check">[x]</span>
        <div>
          <strong>{{ entry.label }}</strong>
          <span>{{ entry.value }}</span>
        </div>
      </div>
    </div>
    <p v-else class="print-empty">{{ emptyText }}</p>
  `,
};
