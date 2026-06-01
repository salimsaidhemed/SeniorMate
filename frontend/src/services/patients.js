import { apiRequest } from "./http.js";
import { withQuery } from "./query.js";

export async function listPatients(params = {}) {
  return apiRequest(withQuery("/patients", params));
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
