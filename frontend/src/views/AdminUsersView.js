import { computed, onMounted, ref } from "vue";

import {
  createUser,
  deleteUser,
  disableUser,
  enableUser,
  listRoles,
  listUsers,
  resetUserPassword,
  updateUser,
  updateUserRoles,
} from "../services/users.js";


const EMPTY_FORM = {
  username: "",
  email: "",
  first_name: "",
  last_name: "",
  enabled: true,
  email_verified: false,
  password: "",
  temporary_password: true,
  roles: [],
};

export default {
  setup() {
    const users = ref([]);
    const roles = ref([]);
    const loading = ref(true);
    const saving = ref(false);
    const actionLoading = ref(false);
    const error = ref("");
    const success = ref("");
    const errors = ref({});
    const editorOpen = ref(false);
    const passwordOpen = ref(false);
    const confirmDisable = ref(false);
    const confirmDelete = ref(false);
    const selectedUser = ref(null);
    const form = ref({ ...EMPTY_FORM });
    const password = ref("");
    const search = ref("");

    const editing = computed(() => Boolean(selectedUser.value));
    const filteredUsers = computed(() => {
      const query = search.value.trim().toLowerCase();
      if (!query) return users.value;
      return users.value.filter((user) =>
        [
          user.username,
          user.email,
          user.first_name,
          user.last_name,
          ...(user.roles || []),
        ]
          .filter(Boolean)
          .some((value) => value.toLowerCase().includes(query)),
      );
    });
    const headers = [
      { title: "User", key: "identity" },
      { title: "Email", key: "email" },
      { title: "Roles", key: "roles", sortable: false },
      { title: "Status", key: "enabled" },
      { title: "Actions", key: "actions", sortable: false, align: "end" },
    ];

    function displayName(user) {
      return [user.first_name, user.last_name].filter(Boolean).join(" ")
        || user.username;
    }

    async function load() {
      loading.value = true;
      error.value = "";
      try {
        const [userResponse, roleResponse] = await Promise.all([
          listUsers(),
          listRoles(),
        ]);
        users.value = userResponse.data;
        roles.value = roleResponse.data;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    }

    function openCreate() {
      selectedUser.value = null;
      form.value = { ...EMPTY_FORM, roles: [] };
      errors.value = {};
      editorOpen.value = true;
    }

    function openEdit(user) {
      selectedUser.value = user;
      form.value = {
        ...EMPTY_FORM,
        ...user,
        password: "",
        roles: [...(user.roles || [])],
      };
      errors.value = {};
      editorOpen.value = true;
    }

    async function save() {
      error.value = "";
      success.value = "";
      errors.value = {};
      saving.value = true;
      try {
        if (editing.value) {
          const payload = { ...form.value };
          delete payload.password;
          delete payload.temporary_password;
          delete payload.roles;
          await updateUser(selectedUser.value.id, payload);
          await updateUserRoles(selectedUser.value.id, form.value.roles);
          success.value = "User details and roles updated.";
        } else {
          await createUser(form.value);
          success.value = "User created with a temporary password.";
        }
        editorOpen.value = false;
        await load();
      } catch (err) {
        error.value = err.message;
        errors.value = err.payload?.errors || {};
      } finally {
        saving.value = false;
      }
    }

    async function setEnabled(user, enabled) {
      actionLoading.value = true;
      error.value = "";
      try {
        if (enabled) {
          await enableUser(user.id);
          success.value = `${displayName(user)} enabled.`;
        } else {
          await disableUser(user.id);
          success.value = `${displayName(user)} disabled.`;
        }
        confirmDisable.value = false;
        await load();
      } catch (err) {
        error.value = err.message;
      } finally {
        actionLoading.value = false;
      }
    }

    function requestDisable(user) {
      selectedUser.value = user;
      confirmDisable.value = true;
    }

    function requestDelete(user) {
      selectedUser.value = user;
      confirmDelete.value = true;
    }

    async function removeUser() {
      actionLoading.value = true;
      error.value = "";
      try {
        await deleteUser(selectedUser.value.id);
        success.value = `${displayName(selectedUser.value)} deleted.`;
        confirmDelete.value = false;
        await load();
      } catch (err) {
        error.value = err.message;
      } finally {
        actionLoading.value = false;
      }
    }

    function openPasswordReset(user) {
      selectedUser.value = user;
      password.value = "";
      passwordOpen.value = true;
    }

    async function resetPassword() {
      if (!password.value) {
        errors.value = { password: "Enter a temporary password." };
        return;
      }
      actionLoading.value = true;
      error.value = "";
      try {
        await resetUserPassword(selectedUser.value.id, password.value, true);
        success.value = `Temporary password set for ${displayName(selectedUser.value)}.`;
        passwordOpen.value = false;
        password.value = "";
      } catch (err) {
        error.value = err.message;
      } finally {
        actionLoading.value = false;
      }
    }

    onMounted(load);

    return {
      actionLoading,
      confirmDelete,
      confirmDisable,
      displayName,
      editing,
      editorOpen,
      error,
      errors,
      filteredUsers,
      form,
      headers,
      loading,
      openCreate,
      openEdit,
      openPasswordReset,
      password,
      passwordOpen,
      removeUser,
      requestDelete,
      requestDisable,
      resetPassword,
      roles,
      save,
      saving,
      search,
      selectedUser,
      setEnabled,
      success,
    };
  },
  template: `
    <div class="page-shell">
      <PageHeader
        title="Users"
        subtitle="Manage Keycloak identities, access status, and SeniorMate roles."
        icon="mdi-account-cog-outline"
      >
        <template #actions>
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-account-plus-outline"
            @click="openCreate"
          >
            Create user
          </v-btn>
        </template>
      </PageHeader>

      <ErrorAlert :message="error" />
      <v-alert
        v-if="success"
        type="success"
        variant="tonal"
        closable
        class="mb-5"
        @click:close="success = ''"
      >
        {{ success }}
      </v-alert>

      <LoadingState v-if="loading" text="Loading Keycloak users..." />

      <v-card v-else class="data-card">
        <v-card-text class="pb-0">
          <v-text-field
            v-model="search"
            label="Search users"
            placeholder="Name, username, email, or role"
            prepend-inner-icon="mdi-magnify"
            clearable
            hide-details
            max-width="440"
          />
        </v-card-text>
        <v-data-table
          :headers="headers"
          :items="filteredUsers"
          item-value="id"
          class="mt-3"
        >
          <template #item.identity="{ item }">
            <div class="py-2">
              <div class="font-weight-medium">{{ displayName(item) }}</div>
              <div class="text-caption text-medium-emphasis">@{{ item.username }}</div>
            </div>
          </template>
          <template #item.email="{ item }">
            <div>{{ item.email }}</div>
            <v-chip
              v-if="item.email_verified"
              size="x-small"
              color="success"
              variant="tonal"
              class="mt-1"
            >
              Verified email
            </v-chip>
          </template>
          <template #item.roles="{ item }">
            <div class="d-flex ga-1 flex-wrap">
              <v-chip
                v-for="role in item.roles"
                :key="role"
                size="small"
                color="secondary"
                variant="tonal"
              >
                {{ role }}
              </v-chip>
              <span v-if="!item.roles?.length" class="text-medium-emphasis">No role</span>
            </div>
          </template>
          <template #item.enabled="{ item }">
            <StatusChip :status="item.enabled ? 'active' : 'inactive'" />
          </template>
          <template #item.actions="{ item }">
            <div class="table-actions">
              <v-tooltip text="Edit user">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-pencil-outline"
                    variant="text"
                    aria-label="Edit user"
                    @click="openEdit(item)"
                  />
                </template>
              </v-tooltip>
              <v-tooltip :text="item.enabled ? 'Disable user' : 'Enable user'">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    :icon="item.enabled ? 'mdi-account-off-outline' : 'mdi-account-check-outline'"
                    variant="text"
                    :color="item.enabled ? 'warning' : 'success'"
                    :aria-label="item.enabled ? 'Disable user' : 'Enable user'"
                    @click="item.enabled ? requestDisable(item) : setEnabled(item, true)"
                  />
                </template>
              </v-tooltip>
              <v-tooltip text="Reset password">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-lock-reset"
                    variant="text"
                    aria-label="Reset password"
                    @click="openPasswordReset(item)"
                  />
                </template>
              </v-tooltip>
              <v-tooltip text="Delete user">
                <template #activator="{ props }">
                  <v-btn
                    v-bind="props"
                    icon="mdi-delete-outline"
                    variant="text"
                    color="error"
                    aria-label="Delete user"
                    @click="requestDelete(item)"
                  />
                </template>
              </v-tooltip>
            </div>
          </template>
          <template #no-data>
            <EmptyState
              icon="mdi-account-search-outline"
              title="No users found"
              message="Create a user or adjust the search."
            />
          </template>
        </v-data-table>
      </v-card>

      <v-dialog v-model="editorOpen" max-width="760">
        <v-card>
          <v-card-title>
            {{ editing ? 'Edit user' : 'Create user' }}
          </v-card-title>
          <v-card-text>
            <v-alert type="info" variant="tonal" class="mb-5">
              User credentials remain in Keycloak. SeniorMate never stores passwords.
            </v-alert>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.username"
                  label="Username *"
                  :error-messages="errors.username"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.email"
                  label="Email *"
                  type="email"
                  :error-messages="errors.email"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.first_name" label="First name" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.last_name" label="Last name" />
              </v-col>
              <v-col v-if="!editing" cols="12">
                <v-text-field
                  v-model="form.password"
                  label="Temporary password *"
                  type="password"
                  autocomplete="new-password"
                  :error-messages="errors.password"
                  hint="The user must change this password after signing in."
                  persistent-hint
                />
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="form.roles"
                  :items="roles"
                  label="SeniorMate roles"
                  multiple
                  chips
                  closable-chips
                  :error-messages="errors.roles"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-switch
                  v-model="form.enabled"
                  color="primary"
                  label="User enabled"
                  hide-details
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-switch
                  v-model="form.email_verified"
                  color="primary"
                  label="Email verified"
                  hide-details
                />
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="editorOpen = false">Cancel</v-btn>
            <v-btn color="primary" variant="flat" :loading="saving" @click="save">
              {{ editing ? 'Save changes' : 'Create user' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="passwordOpen" max-width="500">
        <v-card>
          <v-card-title class="d-flex align-center ga-2">
            <v-icon icon="mdi-lock-reset" color="primary" />
            Reset password
          </v-card-title>
          <v-card-text>
            <p class="mb-4">
              Set a temporary password for {{ selectedUser ? displayName(selectedUser) : 'this user' }}.
              They will be asked to replace it after sign-in.
            </p>
            <v-text-field
              v-model="password"
              label="Temporary password"
              type="password"
              autocomplete="new-password"
              :error-messages="errors.password"
            />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="passwordOpen = false">Cancel</v-btn>
            <v-btn
              color="primary"
              variant="flat"
              :loading="actionLoading"
              @click="resetPassword"
            >
              Reset password
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <ConfirmDialog
        v-model="confirmDisable"
        title="Disable user?"
        :message="'Disable ' + (selectedUser ? displayName(selectedUser) : 'this user') + '? They will no longer be able to sign in.'"
        confirm-label="Disable user"
        :loading="actionLoading"
        @confirm="setEnabled(selectedUser, false)"
      />

      <ConfirmDialog
        v-model="confirmDelete"
        title="Delete user?"
        :message="'Permanently delete ' + (selectedUser ? displayName(selectedUser) : 'this user') + ' from Keycloak? This cannot be undone.'"
        confirm-label="Delete user"
        :loading="actionLoading"
        @confirm="removeUser"
      />
    </div>
  `,
};
