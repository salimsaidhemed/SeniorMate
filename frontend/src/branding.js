import { reactive } from "vue";

import { apiBaseUrl } from "./config.js";
import { getPublicBranding } from "./services/branding.js";


export const DEFAULT_BRANDING = {
  organization_name: "",
  app_display_name: "SeniorMate",
  primary_color: "#1F6F68",
  secondary_color: "#4D6D78",
  accent_color: "#32817A",
  sidebar_color: "#FFFFFF",
  login_banner_text: "",
  footer_text: "",
  has_custom_logo: false,
  logo_url: null,
  updated_at: null,
};

export const defaultLogoUrl = new URL(
  "./assets/branding/logo-concepts/01-care-cross-wordmark.svg",
  import.meta.url,
).href;

export const brandingState = reactive({
  ...DEFAULT_BRANDING,
  logo_src: defaultLogoUrl,
  loaded: false,
  error: "",
});

let vuetifyInstance;

function absoluteLogoUrl(path, updatedAt) {
  if (!path) return defaultLogoUrl;
  const apiOrigin = apiBaseUrl.replace(/\/api\/?$/, "");
  const version = updatedAt ? `?v=${encodeURIComponent(updatedAt)}` : "";
  return `${apiOrigin}${path}${version}`;
}

export function applyBranding(data = {}) {
  Object.assign(brandingState, DEFAULT_BRANDING, data);
  brandingState.logo_src = absoluteLogoUrl(
    brandingState.logo_url,
    brandingState.updated_at,
  );
  brandingState.loaded = true;
  document.title = brandingState.organization_name
    ? `${brandingState.app_display_name} | ${brandingState.organization_name}`
    : brandingState.app_display_name;
  document.documentElement.style.setProperty(
    "--seniormate-primary",
    brandingState.primary_color,
  );
  document.documentElement.style.setProperty(
    "--seniormate-sidebar",
    brandingState.sidebar_color,
  );

  if (vuetifyInstance) {
    const colors =
      vuetifyInstance.theme.themes.value.seniorMateLight.colors;
    colors.primary = brandingState.primary_color;
    colors.secondary = brandingState.secondary_color;
    colors.accent = brandingState.accent_color;
  }
}

export function useDefaultLogo() {
  brandingState.logo_src = defaultLogoUrl;
}

export function bindVuetifyBranding(vuetify) {
  vuetifyInstance = vuetify;
  const colors = vuetifyInstance.theme.themes.value.seniorMateLight.colors;
  colors.primary = brandingState.primary_color;
  colors.secondary = brandingState.secondary_color;
  colors.accent = brandingState.accent_color;
}

export async function initializeBranding() {
  try {
    const response = await getPublicBranding();
    applyBranding(response.data);
  } catch (error) {
    brandingState.error = error.message;
    applyBranding(DEFAULT_BRANDING);
  }
}
