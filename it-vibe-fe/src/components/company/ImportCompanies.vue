<template>
  <div class="manage-company-container">
    <h1 @click="toggleCollapse" class="collapsible-header">
      Import Companies
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
          <label for="importFile">Select File:</label>
          <input
            id="importFile"
            type="file"
            accept=".json"
            @change="handleFileChange"
          />
          <button type="button" @click="importCompanies">
            Import Companies
          </button>
        </div>
      </div>
    </transition>
    <generic-modal
      v-if="modal.show"
      :isOpen="modal.show"
      :message="modal.message"
      :title="modal.title"
      @close="modal.show = false"
    >
      <div>
        <h2>{{ modal.title }}</h2>
        <p>{{ modal.message }}</p>
        <div class="spinner" v-if="importLoading"></div>
        <div v-if="modal.details">
          <h3>Details:</h3>
          <!-- for earch  key in the details oject show key and list if errors -->
          <ul>
            <li v-for="(error, key) in modal.details" :key="key">
              <strong>{{ key }}:</strong>
              <ul>
                <li class="error" v-for="(msg, index) in error" :key="index">
                  {{ msg }}
                </li>
              </ul>
            </li>
          </ul>
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
      modal: {
        show: false,
        message: "",
        title: "",
        details: null,
      },
      importLoading: false,
      selectedFile: null,
    };
  },
  methods: {
    handleFileChange(event) {
      this.errorMessage = "";
      const file = event.target.files[0];

      if (!file) {
        this.selectedFile = null;
        return;
      }

      // Check file extension
      if (!file.name.endsWith(".json")) {
        this.errorMessage = "Please upload a JSON file";
        this.selectedFile = null;
        return;
      }

      this.selectedFile = file;
    },
    async importCompanies() {
      if (!this.selectedFile) {
        this.errorMessage = "Please select a JSON file first";
        return;
      }

      this.importLoading = true;
      this.modal = {
        show: true,
        message: "Importing companies...",
        title: "Info",
      };

      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        const token = sessionStorage.getItem("idToken");

        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const response = await fetch(`${this.apibaseUrl}/companies/import`, {
          method: "POST",
          body: formData,
          headers: headers,
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.modal.message =
            errorData.message || "Failed to import companies";
          this.modal.title = "Error";
          this.modal.details = errorData.details || null;
          throw new Error(this.modal.message);
        }

        const data = await response.json();
        this.modal = {
          show: true,
          message: data.message || "Companies imported successfully",
          title: "Success",
        };
      } catch (error) {
        console.error("Import failed:", error);
      } finally {
        this.importLoading = false;
        this.selectedFile = null;
        document.getElementById("importFile").value = ""; // Reset file input
      }
    },

    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
    },
  },
};
</script>
<style scoped>
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

.form-group {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input[type="file"] {
  padding: 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  background-color: #f8f9fa;
  font-size: 0.9rem;
}

input[type="file"]::file-selector-button {
  padding: 8px 12px;
  background-color: #e9ecef;
  border: 1px solid #ced4da;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 12px;
  transition: background-color 0.2s;
}

input[type="file"]::file-selector-button:hover {
  background-color: #dee2e6;
}

button {
  align-self: flex-start;
}

button:hover {
  background-color: #3a5a9f;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.spinner {
  margin: 20px auto;
  width: 30px;
  height: 30px;
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #4a6baf;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .manage-company-container {
    margin: 10px;
    border-radius: 6px;
  }

  .collapsible-header {
    padding: 14px 16px;
    font-size: 1.1rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .form-group {
    padding: 16px;
  }
}
</style>
