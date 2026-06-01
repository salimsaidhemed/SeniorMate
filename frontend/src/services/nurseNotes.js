import { apiRequest } from "./http.js";

export async function listNurseNotes() {
  return apiRequest("/nurse-notes");
}

export async function getNurseNote(id) {
  return apiRequest(`/nurse-notes/${id}`);
}

export async function createNurseNote(nurseNote) {
  return apiRequest("/nurse-notes", {
    method: "POST",
    body: JSON.stringify(nurseNote),
  });
}

export async function updateNurseNote(id, nurseNote) {
  return apiRequest(`/nurse-notes/${id}`, {
    method: "PUT",
    body: JSON.stringify(nurseNote),
  });
}

export async function deleteNurseNote(id) {
  return apiRequest(`/nurse-notes/${id}`, {
    method: "DELETE",
  });
}

export async function getPatientNurseNotes(patientId) {
  return apiRequest(`/patients/${patientId}/nurse-notes`);
}

export async function getVisitNurseNote(visitId) {
  return apiRequest(`/visits/${visitId}/nurse-note`);
}
