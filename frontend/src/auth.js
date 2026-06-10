import Keycloak from "keycloak-js";
import { reactive } from "vue";

import { authConfig } from "./config.js";

let keycloak;
let refreshTimer;

export const authState = reactive({
  ready: false,
  enabled: authConfig.enabled,
  authenticated: false,
  profile: null,
  roles: [],
  tokenAvailable: false,
  error: "",
});

function rolesFromToken(tokenParsed = {}) {
  const roles = new Set(tokenParsed.realm_access?.roles || []);
  const clientRoles =
    tokenParsed.resource_access?.[authConfig.apiClientId]?.roles || [];
  clientRoles.forEach((role) => roles.add(role));
  return [...roles].filter((role) =>
    ["admin", "manager", "nurse", "caregiver", "viewer"].includes(role),
  );
}

function syncState() {
  const token = keycloak?.tokenParsed || {};
  authState.authenticated = Boolean(keycloak?.authenticated);
  authState.tokenAvailable = Boolean(keycloak?.token);
  authState.roles = rolesFromToken(token);
  authState.profile = authState.authenticated
    ? {
        id: token.sub,
        username: token.preferred_username,
        name: token.name || token.preferred_username || "SeniorMate user",
        email: token.email,
      }
    : null;
}

function clearOidcCallbackParameters() {
  const url = new URL(window.location.href);
  const callbackParameters = [
    "code",
    "error",
    "error_description",
    "iss",
    "session_state",
    "state",
  ];
  const hadCallback = callbackParameters.some((key) => url.searchParams.has(key));
  callbackParameters.forEach((key) => url.searchParams.delete(key));
  if (hadCallback) {
    window.history.replaceState(
      window.history.state,
      document.title,
      `${url.pathname}${url.search}${url.hash}`,
    );
  }
}

async function refreshToken(minValidity = 30) {
  if (!authConfig.enabled || !keycloak?.authenticated) {
    return null;
  }
  await keycloak.updateToken(minValidity);
  syncState();
  return keycloak.token;
}

export async function initializeAuth() {
  if (!authConfig.enabled) {
    authState.authenticated = true;
    authState.profile = {
      id: "development-user",
      username: "development",
      name: "Development User",
      email: null,
    };
    authState.roles = ["admin"];
    authState.ready = true;
    return;
  }

  try {
    keycloak = new Keycloak({
      url: authConfig.url,
      realm: authConfig.realm,
      clientId: authConfig.clientId,
    });
    await keycloak.init({
      onLoad: "login-required",
      pkceMethod: "S256",
      responseMode: "query",
      checkLoginIframe: false,
    });
    clearOidcCallbackParameters();
    syncState();
    keycloak.onTokenExpired = () => {
      refreshToken(30).catch(() => keycloak.login());
    };
    keycloak.onAuthLogout = syncState;
    refreshTimer = window.setInterval(() => {
      refreshToken(60).catch(() => keycloak.login());
    }, 30000);
  } catch (error) {
    authState.error =
      "Authentication is unavailable. Check the Keycloak service and configuration.";
    throw error;
  } finally {
    authState.ready = true;
  }
}

export async function getAccessToken() {
  return refreshToken();
}

export function hasAnyRole(roles = []) {
  return roles.length === 0 || roles.some((role) => authState.roles.includes(role));
}

export function login() {
  if (keycloak) {
    return keycloak.login();
  }
  return Promise.resolve();
}

export function logout() {
  if (refreshTimer) {
    window.clearInterval(refreshTimer);
  }
  if (keycloak) {
    return keycloak.logout({ redirectUri: window.location.origin });
  }
  return Promise.resolve();
}
