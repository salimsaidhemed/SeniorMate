import { apiBaseUrl } from "../config.js";
import { getAccessToken } from "../auth.js";

export async function parseResponse(response) {
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message = payload.message || "The request could not be completed.";
    const error = new Error(message);
    error.payload = payload;
    throw error;
  }

  return payload;
}

export async function apiRequest(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const token = await getAccessToken();
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    headers: {
      ...(!isFormData ? { "Content-Type": "application/json" } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  return parseResponse(response);
}

export async function apiBlobRequest(path, options = {}) {
  const token = await getAccessToken();
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    await parseResponse(response);
  }
  return response.blob();
}
