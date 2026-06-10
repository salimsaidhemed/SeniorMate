import { apiBlobRequest, apiRequest } from "./http.js";


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
  return apiBlobRequest(`/medical-records/${id}/download`);
}
