import { apiRequest } from "./http.js";

export async function getDashboardStats() {
  return apiRequest("/dashboard/stats");
}
