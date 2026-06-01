import { ref } from "vue";

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

    return {
      drawer,
      navItems,
    };
  },
  template: `
    <v-app>
      <v-navigation-drawer v-model="drawer" width="248">
        <v-list density="comfortable" nav>
          <v-list-item
            v-for="item in navItems"
            :key="item.to"
            :prepend-icon="item.icon"
            :title="item.title"
            :to="item.to"
            rounded="0"
          />
        </v-list>
      </v-navigation-drawer>

      <v-app-bar flat border>
        <v-app-bar-nav-icon @click="drawer = !drawer" />
        <v-app-bar-title>SeniorMate</v-app-bar-title>
      </v-app-bar>

      <v-main>
        <router-view />
      </v-main>
    </v-app>
  `,
};
