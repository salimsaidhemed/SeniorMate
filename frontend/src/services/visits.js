import { apiRequest } from "./http.js";
import { withQuery } from "./query.js";

export async function listVisits(params = {}) {
  return apiRequest(withQuery("/visits", params));
}

export async function getVisit(id) {
  return apiRequest(`/visits/${id}`);
}

export async function createVisit(visit) {
  return apiRequest("/visits", {
    method: "POST",
    body: JSON.stringify(visit),
  });
}

export async function updateVisit(id, visit) {
  return apiRequest(`/visits/${id}`, {
    method: "PUT",
    body: JSON.stringify(visit),
  });
}

export async function deleteVisit(id) {
  return apiRequest(`/visits/${id}`, {
    method: "DELETE",
  });
}

export async function listPatientVisits(patientId) {
  return apiRequest(`/patients/${patientId}/visits`);
}
