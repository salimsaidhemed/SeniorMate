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
    <div class="page-header">
      <div class="page-header__copy">
        <div v-if="icon" class="page-header__icon" aria-hidden="true">
          <v-icon :icon="icon" size="22" />
        </div>
        <div>
          <h1 class="page-header__title">{{ title }}</h1>
          <p v-if="subtitle" class="page-header__subtitle">{{ subtitle }}</p>
        </div>
      </div>
      <div class="page-header__actions">
        <slot name="actions" />
      </div>
    </div>
  `,
};
