<template>
  <div class="manage-company-container">
    <h1 @click="toggleCollapse" class="collapsible-header">
      Update or Delete Company
      <span
        class="fa"
        :class="{
          'fa-chevron-right': isCollapsed,
          'fa-chevron-down': !isCollapsed,
        }"
      ></span>
    </h1>
    <transition name="fade-slide">
      <div v-show="!isCollapsed">
        <div class="form-group">
          <label for="companyId">Company ID</label>
          <input
            type="text"
            id="companyId"
            v-model="searchForm.companyId"
            @input="
              company = null;
              originalCompany = null;
              resetChangedFields();
            "
            required
          />
        </div>
        <div class="form-group">
          <button
            type="button"
            :disabled="searchForm.companyId.length < 1"
            @click="searchCompany"
          >
            Search
          </button>
        </div>
        <div v-if="company">
          <div v-if="!company.deletedBy" class="form-group">
            <button
              type="button"
              class="delete"
              v-if="company"
              @click="isDeleting = true"
            >
              Delete
            </button>
          </div>
          <div v-else>
            <span class="deleted-message"> Deleted </span>
          </div>
        </div>

        <div v-if="this.company">
          <div class="form-group" :class="{ changed: changedFields.name }">
            <label for="companyName">Company Name</label>
            <input
              type="text"
              id="companyName"
              v-model="company.name"
              @input="markFieldChanged('name')"
              required
            />
          </div>
          <!-- industry -->
          <div class="form-group" :class="{ changed: changedFields.industry }">
            <label for="industry">Industry</label>
            <input
              type="text"
              id="industry"
              v-model="company.industry"
              @input="markFieldChanged('industry')"
              required
            />
          </div>
          <div class="form-group" :class="{ changed: changedFields.country }">
            <label for="country">Country</label>
            <input
              type="text"
              id="country"
              v-model="company.country"
              @input="markFieldChanged('country')"
              required
            />
          </div>
          <!-- size -->
          <div class="form-group" :class="{ changed: changedFields.size }">
            <label for="size">Size</label>
            <input
              type="text"
              id="size"
              v-model="company.size"
              @input="markFieldChanged('size')"
              required
            />
          </div>
          <!-- revenue -->
          <div class="form-group" :class="{ changed: changedFields.revenue }">
            <label for="revenue">Revenue</label>
            <input
              type="text"
              id="revenue"
              v-model="company.revenue"
              @input="markFieldChanged('revenue')"
              required
            />
          </div>
          <!-- creationDate -->
          <div
            class="form-group"
            :class="{ changed: changedFields.creationDate }"
          >
            <label for="creationDate">Creation Date</label>
            <input
              type="date"
              id="creationDate"
              v-model="company.creationDate"
              @input="markFieldChanged('creationDate')"
              required
            />
          </div>
          <!-- address -->
          <div class="form-group" :class="{ changed: changedFields.adress }">
            <label for="adress">Adress</label>
            <input
              type="text"
              id="adress"
              v-model="company.adress"
              @input="markFieldChanged('adress')"
              required
            />
          </div>
          <!-- siren -->
          <div class="form-group" :class="{ changed: changedFields.siren }">
            <label for="siren">SIREN</label>
            <input
              type="text"
              id="siren"
              v-model="company.siren"
              @input="markFieldChanged('siren')"
              required
            />
          </div>
          <!-- siret -->
          <div class="form-group" :class="{ changed: changedFields.siret }">
            <label for="siret">SIRET</label>
            <input
              type="text"
              id="siret"
              v-model="company.siret"
              @input="markFieldChanged('siret')"
              required
            />
          </div>
          <div class="form-group">
            <button type="button" @click="updateCompany">Save</button>
          </div>
          <div class="form-group">
            <!-- Visible only if atleast one field changed -->
            <button
              type="button"
              v-if="Object.values(changedFields).some((changed) => changed)"
              class="cancel"
              @click="cancelUpdate"
            >
              Cancel
            </button>
          </div>
        </div>
        <div v-else-if="this.searchLoading" class="spinner"></div>
      </div>
    </transition>
    <generic-modal
      v-if="this.modal.show"
      :isOpen="this.modal.show"
      @close="this.modal.show = false"
    >
      <div v-if="this.updateLoading" class="spinner"></div>
      <div>
        <h3>{{ modal.title }}</h3>
        <p>{{ modal.message }}</p>
      </div>
    </generic-modal>
    <generic-modal
      v-if="this.isDeleting"
      :isOpen="this.isDeleting"
      @close="isDeleting = false"
    >
      <div>
        <div style="margin: 10px 0">
          <span>Are you shure you want to delete this company ?</span>
        </div>
        <div class="form-group">
          <button style="margin: 0px 5px" @click="deleteCompany">YES</button>
          <button
            style="margin: 0px 5px"
            class="cancel"
            @click="isDeleting = false"
          >
            NO
          </button>
        </div>
      </div>
    </generic-modal>
  </div>
</template>

<script>
// eslint-disable-next-line
import GenericModal from "@/components/ui/GenericModal.vue";
export default {
  name: "PatchCompany",
  components: {
    GenericModal,
  },
  data() {
    return {
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
      isCollapsed: true,
      isDeleting: false,
      searchForm: {
        companyId: "",
      },
      company: null,
      originalCompany: null,
      changedFields: {
        name: false,
        industry: false,
        country: false,
        size: false,
        revenue: false,
        creationDate: false,
        adress: false,
        siren: false,
        siret: false,
      },
      modal: {
        show: false,
        message: "",
        title: "",
      },
      updateLoading: false,
      searchLoading: false,
    };
  },
  methods: {
    async searchCompany() {
      try {
        this.searchLoading = true;
        const response = await fetch(
          `${this.apibaseUrl}/companies/${this.searchForm.companyId}`
        );
        this.searchLoading = false;
        if (response.ok) {
          this.company = await response.json();
          this.originalCompany = JSON.parse(JSON.stringify(this.company));
          this.resetChangedFields();
        } else if (response.status === 404) {
          this.modal = {
            show: true,
            message: "Company not found",
            title: "Error",
          };
        } else if (response.status === 400) {
          this.modal = {
            show: true,
            message: "Invalid company ID",
            title: "Error",
          };
        } else {
          this.modal = {
            show: true,
            message: "Error fetching company data",
            title: "Error",
          };
        }
      } catch (error) {
        console.error("Error:", error);
        this.modal = {
          show: true,
          message: "Error fetching company data",
          title: "Error",
        };
      }
    },
    async updateCompany() {
      try {
        const payload = {};
        for (const field in this.changedFields) {
          if (this.changedFields[field]) {
            payload[field] = this.company[field];
          }
        }

        if (Object.keys(payload).length === 0) {
          this.modal = {
            show: true,
            message: "No changes made to update",
            title: "Info",
          };
          return;
        }
        const token = localStorage.getItem("idToken");
        this.updateLoading = true;
        this.modal = {
          show: true,
          message: "Updating company data...",
          title: "Info",
        };
        const response = await fetch(
          `${this.apibaseUrl}/companies/${this.company.id}`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
          }
        );
        this.updateLoading = false;
        if (response.ok) {
          this.modal = {
            show: true,
            message: "Company updated successfully",
            title: "Success",
          };
          this.company = null;
          this.originalCompany = null;
          this.resetChangedFields();
          this.isCollapsed = true;
          this.searchForm.companyId = "";
        } else {
          if (response.status === 404) {
            this.modal = {
              show: true,
              message: "Company not found",
              title: "Error",
            };
          } else if (response.status === 400) {
            this.modal = {
              show: true,
              message: "Invalid data provided",
              title: "Error",
            };
          } else {
            this.modal = {
              show: true,
              message: "Error updating company data",
              title: "Error",
            };
          }
          console.error("Error updating company data:", response.status);
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    cancelUpdate() {
      this.company = JSON.parse(JSON.stringify(this.originalCompany));
      this.resetChangedFields();
    },

    markFieldChanged(field) {
      this.changedFields[field] = true;
    },
    resetChangedFields() {
      for (const field in this.changedFields) {
        this.changedFields[field] = false;
      }
    },
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
      if (this.isCollapsed) {
        this.resetChangedFields();
        this.company = null;
        this.originalCompany = null;
        this.searchForm.companyId = "";
      }
    },
    deleteCompany() {
      this.isDeleting = false;
      this.modal = {
        show: true,
        message: "Deleting company...",
        title: "Info",
      };
      const token = localStorage.getItem("idToken");
      fetch(`${this.apibaseUrl}/companies/${this.company.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            this.modal = {
              show: true,
              message: "Company deleted successfully",
              title: "Success",
            };
            this.isDeleting = false;
            this.company = null;
            this.originalCompany = null;
            this.resetChangedFields();
            this.isCollapsed = true;
            this.searchForm.companyId = "";
          } else if (response.status === 404) {
            this.modal = {
              show: true,
              message: "Company not found",
              title: "Error",
            };
          } else {
            this.modal = {
              show: true,
              message: "Error deleting company",
              title: "Error",
            };
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          this.modal = {
            show: true,
            message: "Error deleting company",
            title: "Error",
          };
        });
    },
  },
};
</script>
<style scoped>
.changed {
  background-color: #fffde7; /* Light yellow background */
  border-left: 3px solid #ffc107; /* Yellow accent border */
  transition: all 0.3s ease;
}

.changed input {
  font-weight: bold;
  color: #ff6f00; /* Orange text */
}

.form-group {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.manage-company-container {
  max-width: 600px;
  padding: 0;
  margin: 20px auto;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: white;
  overflow: hidden;
}

.collapsible-header {
  cursor: pointer;
  padding: 16px 20px;
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.2s ease;
}

.collapsible-header:hover {
  background-color: #f1f3f5;
}

.collapsible-header .fa {
  font-size: 0.9rem;
  color: #6c757d;
  transition: transform 0.2s ease;
}

input,
textarea {
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc; /* Lighter border for inputs */
  border-radius: 4px; /* Rounded corners for inputs */
  flex: 2; /* Takes more space than the label */
}
label {
  flex: 1; /* Label takes less space compared to input */
  margin-right: 10px; /* Add some spacing between label and input */
  white-space: nowrap; /* Prevent label text from wrapping */
}

textarea {
  resize: vertical; /* Allow vertical resizing of text areas */
}

.collapsible-header {
  cursor: pointer;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.deleted-message {
  color: var(--dark-red);
  font-weight: bold;
  font-size: 1.2em;
  text-align: center;
  margin: 5px 0;
  padding: 5px;
  border: 1px solid var(--dark-red);
  border-radius: 8px;
}
</style>
