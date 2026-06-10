import { apiRequest } from "./http.js";


export function listUsers() {
  return apiRequest("/admin/users");
}

export function getUser(userId) {
  return apiRequest(`/admin/users/${userId}`);
}

export function createUser(user) {
  return apiRequest("/admin/users", {
    method: "POST",
    body: JSON.stringify(user),
  });
}

export function updateUser(userId, user) {
  return apiRequest(`/admin/users/${userId}`, {
    method: "PUT",
    body: JSON.stringify(user),
  });
}

export function enableUser(userId) {
  return apiRequest(`/admin/users/${userId}/enabled`, {
    method: "PATCH",
    body: JSON.stringify({ enabled: true }),
  });
}

export function disableUser(userId) {
  return apiRequest(`/admin/users/${userId}/enabled`, {
    method: "PATCH",
    body: JSON.stringify({ enabled: false }),
  });
}

export function deleteUser(userId) {
  return apiRequest(`/admin/users/${userId}`, {
    method: "DELETE",
  });
}

export function resetUserPassword(userId, password, temporary = true) {
  return apiRequest(`/admin/users/${userId}/reset-password`, {
    method: "POST",
    body: JSON.stringify({ password, temporary }),
  });
}

export function listRoles() {
  return apiRequest("/admin/roles");
}

export function updateUserRoles(userId, roles) {
  return apiRequest(`/admin/users/${userId}/roles`, {
    method: "PUT",
    body: JSON.stringify({ roles }),
  });
}
