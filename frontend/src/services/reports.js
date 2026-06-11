import { apiBlobRequest, apiRequest } from "./http.js";
import { withQuery } from "./query.js";


const reportPaths = {
  "patient-census": "/reports/patient-census",
  "visit-activity": "/reports/visit-activity",
  "staff-activity": "/reports/staff-activity",
  "assessment-summary": "/reports/assessment-summary",
  "medical-records-summary": "/reports/medical-records-summary",
};

export function getReport(reportKey, filters = {}) {
  return apiRequest(withQuery(reportPaths[reportKey], filters));
}

export function exportReportCsv(reportKey, filters = {}) {
  return apiBlobRequest(
    withQuery(reportPaths[reportKey], { ...filters, format: "csv" }),
  );
}
