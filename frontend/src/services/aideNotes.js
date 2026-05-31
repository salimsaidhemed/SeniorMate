import { apiRequest } from "./http.js";

export async function listAideNotes() {
  return apiRequest("/aide-notes");
}

export async function getAideNote(id) {
  return apiRequest(`/aide-notes/${id}`);
}

export async function createAideNote(aideNote) {
  return apiRequest("/aide-notes", {
    method: "POST",
    body: JSON.stringify(aideNote),
  });
}

export async function updateAideNote(id, aideNote) {
  return apiRequest(`/aide-notes/${id}`, {
    method: "PUT",
    body: JSON.stringify(aideNote),
  });
}

export async function deleteAideNote(id) {
  return apiRequest(`/aide-notes/${id}`, {
    method: "DELETE",
  });
}

export async function getPatientAideNotes(patientId) {
  return apiRequest(`/patients/${patientId}/aide-notes`);
}

export async function getVisitAideNote(visitId) {
  return apiRequest(`/visits/${visitId}/aide-note`);
}
