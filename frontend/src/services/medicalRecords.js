import { apiBaseUrl } from "../config.js";
import { apiRequest, parseResponse } from "./http.js";


export async function listMedicalRecords() {
  return apiRequest("/medical-records");
}

export async function getMedicalRecord(id) {
  return apiRequest(`/medical-records/${id}`);
}

export async function uploadMedicalRecord(medicalRecord) {
  const formData = new FormData();
  Object.entries(medicalRecord).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== "") {
      formData.append(key, value);
    }
  });

  return apiRequest("/medical-records", {
    method: "POST",
    body: formData,
  });
}

export async function updateMedicalRecord(id, medicalRecord) {
  return apiRequest(`/medical-records/${id}`, {
    method: "PUT",
    body: JSON.stringify(medicalRecord),
  });
}

export async function deleteMedicalRecord(id) {
  return apiRequest(`/medical-records/${id}`, {
    method: "DELETE",
  });
}

export async function getPatientMedicalRecords(patientId) {
  return apiRequest(`/patients/${patientId}/medical-records`);
}

export async function downloadMedicalRecord(id) {
  const response = await fetch(`${apiBaseUrl}/medical-records/${id}/download`);
  if (!response.ok) {
    await parseResponse(response);
  }
  return response.blob();
}
