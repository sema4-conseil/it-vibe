<template>
  <div class="manage-company-container">
    <h1 @click="toggleCollapse" class="collapsible-header">
      Create Company
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
        <form @submit.prevent="saveCompany">
          <div v-for="(field, index) in fields" :key="index" class="form-group">
            <label :for="field.name">{{ field.label }}</label>
            <input
              v-if="field.type !== 'textarea'"
              :type="field.type"
              :id="field.name"
              v-model="form[field.name]"
              :required="field.required"
            />
            <textarea
              v-else
              :id="field.name"
              v-model="form[field.name]"
              :required="field.required"
            ></textarea>
          </div>
          <button type="submit">Create Company</button>
        </form>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "CreateCompany",
  data() {
    return {
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
      isCollapsed: true,
      fields: [
        { name: "name", label: "Company Name", type: "text", required: true },
        { name: "industry", label: "Industry", type: "text", required: true },
        { name: "country", label: "Country", type: "text", required: true },
        { name: "size", label: "Size", type: "text", required: true },
        { name: "revenue", label: "Revenue", type: "text", required: true },
        {
          name: "creationDate",
          label: "Creation Date",
          type: "date",
          required: true,
        },
        { name: "adress", label: "Address", type: "text", required: true },
        { name: "siren", label: "SIREN", type: "text", required: true },
        { name: "siret", label: "SIRET", type: "text", required: true },
      ],
      form: {
        name: "",
        location: "",
        size: "",
        revenue: "",
        industry: "",
        description: "",
        country: "",
        creationDate: "",
        updateDate: "",
        adress: "",
        IBAN: "",
        siren: "",
        siret: "",
        president: {
          firstname: "",
          lastname: "",
          phoneNumber: "",
          email: "",
        },
      },
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
    },
    async saveCompany() {
      try {
        // Retrieve the JWT token from session storage
        const token = sessionStorage.getItem("idToken");
        const response = await fetch(`${this.apibaseUrl}/companies/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.form),
        });
        if (!response.ok) {
          throw new Error("Failed to create company");
        }
        this.resetForm();
        alert("Company created successfully!");
      } catch (error) {
        alert("An error occurred while submitting your review.");
      }
    },
    resetForm() {
      this.form = {
        name: "",
        size: "",
        revenue: "",
        industry: "",
        country: "",
        creationDate: "",
        adress: "",
        siren: "",
        siret: "",
      };
      this.isCollapsed = true;
    },
  },
};
</script>

<style scoped>
.form-group {
  display: flex;
  align-items: center; /* Align label and input vertically */
  margin-bottom: 10px; /* Add spacing between form groups */
}
.manage-company-container {
  max-width: 600px;
  padding: 0 5px 5px 5px;
  margin: 10px auto;
  border: 1px solid #e0e0e0; /* Lighter border to match overall style */
  border-radius: 12px; /* Slightly more rounded corners */
  background-color: white; /* White background for cards */
  flex: auto;
  flex-direction: column;
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
.form-group {
  display: flex;
  align-items: center; /* Align label and input vertically */
  margin-bottom: 10px; /* Add spacing between form groups */
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
</style>
