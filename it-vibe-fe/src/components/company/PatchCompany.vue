<template>
  <div class="manage-company-container">
    <h1 @click="toggleCollapse" class="collapsible-header">
      Update Company
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
        const response = await fetch(
          `${this.apibaseUrl}/companies/${this.searchForm.companyId}`
        );
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
        const token = sessionStorage.getItem("idToken");
        this.updateLoading = true;
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
          this.modal = {
            show: true,
            message: "Error updating company data",
            title: "Error",
          };
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
  },
};
</script>
<style scoped>
@import "./styles/styles.css";

.changed {
  background-color: #fffde7; /* Light yellow background */
  border-left: 3px solid #ffc107; /* Yellow accent border */
  transition: all 0.3s ease;
}

.changed input {
  font-weight: bold;
  color: #ff6f00; /* Orange text */
}
</style>
