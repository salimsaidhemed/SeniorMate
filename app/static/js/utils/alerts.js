export function showAlert(containerId, message, type = "success", timeout = 5000) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;

  // Auto-hide after 5 seconds
  setTimeout(() => {
    const alert = container.querySelector(".alert");
    if (alert) alert.classList.remove("show");
    setTimeout(() => (container.innerHTML = ""), 500);
  }, timeout);
}
