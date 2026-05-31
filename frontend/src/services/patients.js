import { apiBaseUrl } from "../config.js";

async function parseResponse(response) {
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message = payload.message || "The request could not be completed.";
    const error = new Error(message);
    error.payload = payload;
    throw error;
  }

  return payload;
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  return parseResponse(response);
}

export async function listPatients() {
  return apiRequest("/patients");
}

export async function getPatient(id) {
  return apiRequest(`/patients/${id}`);
}

export async function createPatient(patient) {
  return apiRequest("/patients", {
    method: "POST",
    body: JSON.stringify(patient),
  });
}

export async function updatePatient(id, patient) {
  return apiRequest(`/patients/${id}`, {
    method: "PUT",
    body: JSON.stringify(patient),
  });
}

export async function deletePatient(id) {
  return apiRequest(`/patients/${id}`, {
    method: "DELETE",
  });
}
