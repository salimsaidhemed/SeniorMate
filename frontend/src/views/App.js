import { computed, ref } from "vue";
import { authState, login, logout } from "../auth.js";

const navItems = [
  { title: "Dashboard", icon: "mdi-view-dashboard-outline", to: "/" },
  { title: "Patients", icon: "mdi-account-heart-outline", to: "/patients" },
  { title: "Visits", icon: "mdi-calendar-clock-outline", to: "/visits" },
  { title: "Aide Notes", icon: "mdi-clipboard-check-outline", to: "/aide-notes" },
  { title: "Nurse Notes", icon: "mdi-clipboard-pulse-outline", to: "/nurse-notes" },
];

export default {
  setup() {
    const drawer = ref(true);
    const displayRole = computed(() => authState.roles[0] || "user");
    const userInitials = computed(() => {
      const name = authState.profile?.name || "";
      return (
        name
          .split(/\s+/)
          .filter(Boolean)
          .slice(0, 2)
          .map((part) => part[0])
          .join("")
          .toUpperCase() || "SM"
      );
    });

    return {
      authState,
      displayRole,
      drawer,
      login,
      logout,
      navItems,
      userInitials,
    };
  },
  template: `
    <v-app>
      <v-navigation-drawer v-model="drawer" width="260" color="surface">
        <div class="app-brand">
          <div class="app-brand__mark">
            <v-icon icon="mdi-heart-pulse" size="22" />
          </div>
          <div>
            <div class="app-brand__name">SeniorMate</div>
            <div class="app-brand__caption">Care operations</div>
          </div>
        </div>

        <v-divider />

        <v-list density="comfortable" nav class="px-3 pt-4">
          <v-list-subheader>Workspace</v-list-subheader>
          <v-list-item
            v-for="item in navItems"
            :key="item.to"
            :prepend-icon="item.icon"
            :title="item.title"
            :to="item.to"
            active-color="primary"
            rounded="lg"
            class="mb-1"
          />
        </v-list>

        <template #append>
          <div class="pa-3">
            <v-list-item
              :title="authState.profile?.name || 'SeniorMate user'"
              :subtitle="displayRole"
              rounded="lg"
            >
              <template #prepend>
                <v-avatar color="primary" size="36">
                  <span class="text-caption font-weight-bold">{{ userInitials }}</span>
                </v-avatar>
              </template>
            </v-list-item>
            <v-btn
              v-if="authState.enabled"
              block
              variant="text"
              color="secondary"
              prepend-icon="mdi-logout"
              class="mt-2"
              @click="logout"
            >
              Log out
            </v-btn>
          </div>
        </template>
      </v-navigation-drawer>

      <v-app-bar flat border color="surface" height="64">
        <v-app-bar-nav-icon aria-label="Toggle navigation" @click="drawer = !drawer" />
        <v-app-bar-title class="text-subtitle-1 font-weight-medium">
          Care workspace
        </v-app-bar-title>
      </v-app-bar>

      <v-main class="app-surface">
        <v-container v-if="authState.error" class="py-12" max-width="720">
          <v-alert type="error" variant="tonal" title="Sign-in unavailable">
            {{ authState.error }}
            <template #append>
              <v-btn variant="text" @click="login">Retry</v-btn>
            </template>
          </v-alert>
        </v-container>
        <router-view v-else />
      </v-main>
    </v-app>
  `,
};
