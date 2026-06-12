<script setup>
import { onMounted, ref } from "vue";

const container = ref(null);
const error = ref("");
const code = `
flowchart TB
  Browser[User browser]
  Vue[Vue 3 + Vuetify]
  Flask[Flask API]
  Postgres[(PostgreSQL)]
  MinIO[(Private MinIO)]
  Keycloak[Keycloak]
  Compose[Docker Compose]

  Browser --> Vue
  Vue -->|Bearer token + API requests| Flask
  Vue -->|OIDC login| Keycloak
  Flask -->|Domain data + metadata| Postgres
  Flask -->|Private documents + images| MinIO
  Flask -->|JWT validation + Admin API| Keycloak
  Compose -. starts the local stack .-> Vue
  Compose -.-> Flask
  Compose -.-> Postgres
  Compose -.-> MinIO
  Compose -.-> Keycloak
`;

onMounted(async () => {
  try {
    const { default: mermaid } = await import("mermaid");
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: "base",
      themeVariables: {
        primaryColor: "#E7F4F1",
        primaryTextColor: "#163632",
        primaryBorderColor: "#0C655F",
        lineColor: "#4E6E69",
        secondaryColor: "#EDF3F8",
        tertiaryColor: "#FFF8E8",
        fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
      }
    });
    const id = `seniormate-diagram-${Math.random().toString(36).slice(2)}`;
    const { svg } = await mermaid.render(id, code);
    container.value.innerHTML = svg;
  } catch {
    error.value = "The architecture diagram could not be rendered.";
  }
});
</script>

<template>
  <div class="mermaid-frame">
    <div ref="container" class="mermaid-output" aria-label="SeniorMate architecture diagram" />
    <p v-if="error" class="mermaid-error">{{ error }}</p>
  </div>
</template>
