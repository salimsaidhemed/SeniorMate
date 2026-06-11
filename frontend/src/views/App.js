import { computed, ref } from "vue";
import { authState, login, logout } from "../auth.js";
import {
  brandingState,
  defaultLogoUrl,
  useDefaultLogo,
} from "../branding.js";
import {
  can,
  canManageBranding,
  canManageUsers,
} from "../permissions.js";
import { appVersion } from "../config.js";

const navItems = [
  {
    title: "Dashboard",
    icon: "mdi-view-dashboard-outline",
    to: "/",
    permission: "dashboard.read",
  },
  {
    title: "Patients",
    icon: "mdi-account-heart-outline",
    to: "/patients",
    permission: "patients.read",
  },
  {
    title: "Visits",
    icon: "mdi-calendar-clock-outline",
    to: "/visits",
    permission: "visits.read",
  },
  {
    title: "Aide Notes",
    icon: "mdi-clipboard-check-outline",
    to: "/aide-notes",
    permission: "aide_notes.read",
  },
  {
    title: "Nurse Notes",
    icon: "mdi-clipboard-pulse-outline",
    to: "/nurse-notes",
    permission: "nurse_notes.read",
  },
  {
    title: "Reports",
    icon: "mdi-chart-box-outline",
    to: "/reports",
    permission: "reports.read",
  },
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
    const visibleNavItems = computed(() =>
      navItems.filter((item) => can(item.permission)),
    );
    const showBrandingSettings = computed(() => canManageBranding());
    const showUserManagement = computed(() => canManageUsers());
    const sidebarTextColor = computed(() => {
      const hex = brandingState.sidebar_color.replace("#", "");
      const [red, green, blue] = [0, 2, 4].map((index) =>
        Number.parseInt(hex.slice(index, index + 2), 16),
      );
      return (red * 299 + green * 587 + blue * 114) / 1000 > 150
        ? "#20302F"
        : "#FFFFFF";
    });

    return {
      appVersion,
      authState,
      brandingState,
      defaultLogoUrl,
      displayRole,
      drawer,
      login,
      logout,
      showBrandingSettings,
      showUserManagement,
      sidebarTextColor,
      useDefaultLogo,
      userInitials,
      visibleNavItems,
    };
  },
  template: `
    <v-app>
      <v-navigation-drawer
        v-model="drawer"
        width="260"
        :color="brandingState.sidebar_color"
        :style="{ color: sidebarTextColor }"
      >
        <div class="app-brand">
          <img
            :src="brandingState.logo_src"
            :alt="brandingState.app_display_name"
            class="app-brand__logo"
            @error="useDefaultLogo"
          />
          <div>
            <div v-if="brandingState.has_custom_logo" class="app-brand__name">
              {{ brandingState.app_display_name }}
            </div>
            <div class="app-brand__caption">
              {{ brandingState.organization_name || 'Care operations' }}
            </div>
          </div>
        </div>

        <v-divider />

        <v-list density="comfortable" nav class="px-3 pt-4">
          <v-list-subheader>Workspace</v-list-subheader>
          <v-list-item
            v-for="item in visibleNavItems"
            :key="item.to"
            :prepend-icon="item.icon"
            :title="item.title"
            :to="item.to"
            active-color="primary"
            rounded="lg"
            class="mb-1"
          />
        </v-list>

        <v-list
          v-if="showUserManagement || showBrandingSettings"
          density="comfortable"
          nav
          class="px-3"
        >
          <v-list-subheader>Settings</v-list-subheader>
          <v-list-item
            v-if="showUserManagement"
            prepend-icon="mdi-account-cog-outline"
            title="Users"
            to="/admin/users"
            color="primary"
            rounded="lg"
          />
          <v-list-item
            v-if="showBrandingSettings"
            prepend-icon="mdi-palette-outline"
            title="Branding"
            to="/settings/branding"
            color="primary"
            rounded="lg"
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
            <div
              v-if="brandingState.footer_text"
              class="app-brand__footer"
            >
              {{ brandingState.footer_text }}
            </div>
            <div class="app-brand__version">
              SeniorMate Version {{ appVersion }}
            </div>
          </div>
        </template>
      </v-navigation-drawer>

      <v-app-bar flat border color="surface" height="64">
        <v-app-bar-nav-icon aria-label="Toggle navigation" @click="drawer = !drawer" />
        <v-app-bar-title class="text-subtitle-1 font-weight-medium">
          {{ brandingState.app_display_name }} workspace
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
