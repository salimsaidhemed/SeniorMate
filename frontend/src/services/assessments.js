import { apiRequest } from "./http.js";


export async function listAssessments() {
  return apiRequest("/assessments");
}

export async function getAssessment(id) {
  return apiRequest(`/assessments/${id}`);
}

export async function createAssessment(assessment) {
  return apiRequest("/assessments", {
    method: "POST",
    body: JSON.stringify(assessment),
  });
}

export async function updateAssessment(id, assessment) {
  return apiRequest(`/assessments/${id}`, {
    method: "PUT",
    body: JSON.stringify(assessment),
  });
}

export async function deleteAssessment(id) {
  return apiRequest(`/assessments/${id}`, {
    method: "DELETE",
  });
}

export async function getPatientAssessments(patientId) {
  return apiRequest(`/patients/${patientId}/assessments`);
}

export async function getVisitAssessments(visitId) {
  return apiRequest(`/visits/${visitId}/assessments`);
}
