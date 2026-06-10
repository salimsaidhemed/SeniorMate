import { apiRequest } from "./http.js";
import { apiBaseUrl } from "../config.js";
import { parseResponse } from "./http.js";

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

export async function uploadPatientPhoto(patientId, file) {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest(`/patients/${patientId}/photo`, {
    method: "POST",
    body: formData,
  });
}

export async function getPatientPhoto(patientId) {
  const response = await fetch(`${apiBaseUrl}/patients/${patientId}/photo`);
  if (!response.ok) {
    await parseResponse(response);
  }
  return response.blob();
}

export async function verifyPatientPhoto(patientId, verified) {
  return apiRequest(`/patients/${patientId}/photo/verify`, {
    method: "PATCH",
    body: JSON.stringify({ verified }),
  });
}

export async function deletePatientPhoto(patientId) {
  return apiRequest(`/patients/${patientId}/photo`, {
    method: "DELETE",
  });
}
