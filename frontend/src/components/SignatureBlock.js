export default {
  props: {
    name: {
      type: String,
      default: "",
    },
    date: {
      type: String,
      default: "",
    },
    signatureData: {
      type: String,
      default: "",
    },
    roleLabel: {
      type: String,
      default: "Staff name",
    },
  },
  template: `
    <div class="signature-block">
      <PrintField :label="roleLabel" :value="name" />
      <PrintField label="Signature date" :value="date" />
      <div class="signature-block__line">
        {{ signatureData || 'Signature on file: not provided' }}
      </div>
    </div>
  `,
};
