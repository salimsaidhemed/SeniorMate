import { computed } from "vue";

import { canViewDashboard } from "../permissions.js";


export default {
  setup() {
    const returnRoute = computed(() =>
      canViewDashboard() ? { name: "dashboard" } : { name: "patients" },
    );
    const returnLabel = computed(() =>
      canViewDashboard() ? "Return to dashboard" : "Return to patients",
    );

    return {
      returnLabel,
      returnRoute,
    };
  },
  template: `
    <div class="page-shell">
      <v-card class="access-denied">
        <v-card-text class="text-center pa-10">
          <v-icon
            icon="mdi-shield-lock-outline"
            color="warning"
            size="58"
            class="mb-5"
          />
          <h1 class="text-h5 font-weight-bold mb-3">Access denied</h1>
          <p class="text-body-1 text-medium-emphasis mb-6">
            Your current SeniorMate role does not allow access to this page.
            Contact an administrator if you believe your access should change.
          </p>
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-arrow-left"
            :to="returnRoute"
          >
            {{ returnLabel }}
          </v-btn>
        </v-card-text>
      </v-card>
    </div>
  `,
};
