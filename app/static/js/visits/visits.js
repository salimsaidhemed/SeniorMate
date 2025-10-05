import { showAlert } from "../utils/alerts.js";

const patientId = window.patientId;
let selectedVisitId = null;

// Load visits with optional filter & pagination
async function loadVisits(page = 1, date = "") {
  const res = await fetch(`/api/visits/${patientId}?page=${page}&date=${date}`);
  const data = await res.json();
  const tbody = document.querySelector("#visitsTable tbody");
  tbody.innerHTML = "";

  if (!data.items || data.items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted">No visits recorded for this patient.</td></tr>`;
  } else {
    data.items.forEach(v => {
      const row = document.createElement("tr");
      row.style.cursor = "pointer";
      row.addEventListener("click", () => selectVisit(v.id));
      row.innerHTML = `
        <td>${v.visit_date}</td>
        <td>${v.visit_type}</td>
        <td>${v.narrative || ''}</td>
        <td><span class="badge bg-primary">#${v.id}</span></td>
      `;
      tbody.appendChild(row);
    });
  }

  // Update pagination
  renderPagination("visitsPagination", data.page, data.pages, loadVisits);
}

// Handle Add Visit form
document.querySelector("#visitForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target).entries());
  formData.patient_id = patientId;

  const res = await fetch("/api/visits/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData)
  });

  if (res.ok) {
    showAlert("visitAlertContainer", "✅ Visit added successfully!", "success");
    e.target.reset();
    loadVisits();
  } else {
    showAlert("visitAlertContainer", "❌ Failed to add visit.", "danger");
  }
});

// Load assessments when visit selected
async function selectVisit(id, page = 1) {
  selectedVisitId = id;
  document.querySelector("#btnAddAssessment").disabled = false;

  const res = await fetch(`/api/visits/${id}/assessments?page=${page}`);
  const data = await res.json();
  const tbody = document.querySelector("#assessmentsTable tbody");
  tbody.innerHTML = "";

  if (!data.items || data.items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">No assessments recorded for this visit.</td></tr>`;
  } else {
    data.items.forEach(a => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${a.created_at}</td>
        <td>${a.aide_name || '—'}</td>
        <td>${a.notes || ''}</td>
      `;
      tbody.appendChild(row);
    });
  }

  renderPagination("assessmentsPagination", data.page, data.pages, (p) => selectVisit(id, p));
}

// Generic pagination renderer
function renderPagination(containerId, currentPage, totalPages, callback) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  if (totalPages <= 1) return;

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.className = `btn btn-sm ${i === currentPage ? 'btn-primary' : 'btn-outline-primary'} me-1`;
    btn.textContent = i;
    btn.onclick = () => callback(i);
    container.appendChild(btn);
  }
}

// Initial load
loadVisits();
