export const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5001/api";

export const appVersion = __APP_VERSION__;

export const authConfig = {
  enabled: import.meta.env.VITE_AUTH_ENABLED !== "false",
  url: import.meta.env.VITE_KEYCLOAK_URL || "http://localhost:8080",
  realm: import.meta.env.VITE_KEYCLOAK_REALM || "seniormate",
  clientId:
    import.meta.env.VITE_KEYCLOAK_CLIENT_ID || "seniormate-frontend",
  apiClientId:
    import.meta.env.VITE_KEYCLOAK_API_CLIENT_ID || "seniormate-api",
};
