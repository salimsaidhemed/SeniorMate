import assert from "node:assert/strict";
import test from "node:test";

import {
  permissionsForRoles,
  rolesCan,
} from "../src/permission-policy.js";


test("admin wildcard grants every permission", () => {
  assert.equal(rolesCan(["admin"], "future.permission"), true);
  assert.equal(rolesCan(["admin"], "user_admin.manage"), true);
});

test("viewer remains read only with report access", () => {
  assert.equal(rolesCan(["viewer"], "patients.read"), true);
  assert.equal(rolesCan(["viewer"], "patients.write"), false);
  assert.equal(rolesCan(["viewer"], "visits.write"), false);
  assert.equal(rolesCan(["viewer"], "reports.read"), true);
});

test("clinical write permissions match the backend map", () => {
  assert.equal(rolesCan(["caregiver"], "aide_notes.write"), true);
  assert.equal(rolesCan(["caregiver"], "nurse_notes.write"), false);
  assert.equal(rolesCan(["nurse"], "nurse_notes.write"), true);
  assert.equal(rolesCan(["nurse"], "medical_records.write"), true);
  assert.equal(rolesCan(["nurse"], "patient_photos.verify"), false);
});

test("settings permissions distinguish managers from admins", () => {
  assert.equal(rolesCan(["manager"], "branding.write"), true);
  assert.equal(rolesCan(["manager"], "user_admin.manage"), false);
  assert.equal(rolesCan(["admin"], "user_admin.manage"), true);
});

test("multiple roles combine their permissions", () => {
  const permissions = permissionsForRoles(["viewer", "caregiver"]);
  assert.equal(permissions.has("dashboard.read"), true);
  assert.equal(permissions.has("aide_notes.write"), true);
});
