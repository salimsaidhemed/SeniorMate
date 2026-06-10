export default {
  props: {
    eyebrow: {
      type: String,
      default: "",
    },
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
    <div class="detail-header">
      <div class="detail-header__identity">
        <slot name="avatar" />
        <div class="detail-header__copy">
          <div v-if="eyebrow" class="detail-header__eyebrow">{{ eyebrow }}</div>
          <h1 class="detail-header__title">{{ title }}</h1>
          <div v-if="subtitle" class="detail-header__subtitle">{{ subtitle }}</div>
          <div class="detail-header__meta">
            <slot name="meta" />
          </div>
        </div>
      </div>
      <div class="detail-header__actions">
        <slot name="actions" />
      </div>
    </div>
  `,
};
