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
@import "./styles/styles.css";
</style>
