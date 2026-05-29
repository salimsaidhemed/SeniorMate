import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

import { createApp, onMounted, ref } from "vue";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";

const App = {
  setup() {
    const health = ref(null);
    const loading = ref(true);
    const error = ref("");

    async function loadHealth() {
      loading.value = true;
      error.value = "";

      try {
        const response = await fetch(`${apiBaseUrl}/health`);
        const payload = await response.json();

        if (!response.ok) {
          throw new Error(payload.status || "Backend health check failed");
        }

        health.value = payload;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    onMounted(loadHealth);

    return {
      apiBaseUrl,
      error,
      health,
      loading,
      loadHealth,
    };
  },
  template: `
    <v-app>
      <v-main>
        <v-container class="py-10" style="max-width: 960px;">
          <v-row align="center" class="mb-6">
            <v-col cols="12" md="8">
              <p class="text-overline mb-2">SeniorMate local development</p>
              <h1 class="text-h3 font-weight-bold mb-3">Care operations dashboard</h1>
              <p class="text-body-1 text-medium-emphasis mb-0">
                Local backend, frontend, PostgreSQL, and MinIO services are wired for development.
              </p>
            </v-col>
            <v-col cols="12" md="4" class="text-md-right">
              <v-btn color="primary" variant="flat" :loading="loading" @click="loadHealth">
                Refresh health
              </v-btn>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="4">
              <v-card variant="tonal">
                <v-card-title>Backend</v-card-title>
                <v-card-text>
                  <div class="text-h5 mb-2">{{ health?.status || "Checking" }}</div>
                  <div class="text-body-2">{{ apiBaseUrl }}</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="4">
              <v-card variant="tonal">
                <v-card-title>Database</v-card-title>
                <v-card-text>
                  <div class="text-h5 mb-2">{{ health?.database || "Checking" }}</div>
                  <div class="text-body-2">PostgreSQL via Docker Compose</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="4">
              <v-card variant="tonal">
                <v-card-title>Storage</v-card-title>
                <v-card-text>
                  <div class="text-h5 mb-2">MinIO</div>
                  <div class="text-body-2">{{ health?.minio_endpoint || "Configured from environment" }}</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-alert v-if="error" type="error" variant="tonal" class="mt-6">
            {{ error }}
          </v-alert>
        </v-container>
      </v-main>
    </v-app>
  `,
};

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: { mdi },
  },
});

createApp(App).use(vuetify).mount("#app");
