import { apiBaseUrl } from "../config.js";
import { apiRequest } from "./http.js";


async function parsePublicResponse(response) {
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.message || "Branding could not be loaded.");
  }
  return payload;
}

export async function getPublicBranding() {
  return parsePublicResponse(await fetch(`${apiBaseUrl}/public/branding`));
}

export async function getBranding() {
  return apiRequest("/settings/branding");
}

export async function updateBranding(branding) {
  return apiRequest("/settings/branding", {
    method: "PUT",
    body: JSON.stringify(branding),
  });
}

export async function uploadBrandingLogo(file) {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest("/settings/branding/logo", {
    method: "POST",
    body: formData,
  });
}

export async function deleteBrandingLogo() {
  return apiRequest("/settings/branding/logo", {
    method: "DELETE",
  });
}
