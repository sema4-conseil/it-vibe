<template>
  <div>
    <!-- Search Panel -->
    <div class="search-container" style="max-width">
      <form @submit.prevent="searchCompanies" class="search-form">
        <div class="form-group">
          <label for="name">Name</label>
          <input
            placeholder="e.g. Tech Corp"
            id="name"
            v-model.trim="searchCriteria.name"
          />
        </div>
        <div class="form-group">
          <label for="siren">SIREN</label>
          <input
            type="text"
            id="siren"
            v-model.trim="searchCriteria.siren"
            placeholder="9-digit SIREN"
            maxlength="9"
          />
        </div>
        <div class="form-group">
          <div class="form-group">
            <label for="siret">SIRET</label>
            <input
              type="text"
              id="siret"
              v-model.trim="searchCriteria.siret"
              placeholder="14-digit SIRET"
              maxlength="14"
            />
          </div>
        </div>
        <div class="button-container">
          <button type="submit"><i class="fa fa-search"></i>Search</button>
        </div>
      </form>
    </div>
    <div v-if="loading">
      <p>Loading companies ...</p>
      <div class="spinner"></div>
    </div>
    <div v-else-if="companies" class="search-results">
      <div v-if="!companies.length">
        <p>No companies found.</p>
      </div>
      <div v-else>
        <p v-if="totalCount > 1">
          found {{ companies.length }} / {{ totalCount }} companies
        </p>
      </div>
      <company-card
        v-for="company in companies"
        :key="company.id"
        :company="company"
        @click="goToCompanyDetails(company.id)"
      ></company-card>
      <div>
        <button @click="fetchCompanies()" :disabled="!lastEvaluatedKey">
          <i class="fa fa-forward"></i>Next Items
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import CompanyCard from "./company/CompanyCard.vue";
export default {
  components: { CompanyCard },
  data() {
    return {
      companies: null,
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
      lastEvaluatedKey: null,
      pageSize: 4,
      totalCount: 0,
      loading: false,
      searchCriteria: {
        name: "",
        siren: "",
        siret: "",
      },
    };
  },
  methods: {
    async fetchCompanies() {
      try {
        this.loading = true;
        let url = `${this.apibaseUrl}/companies?pageSize=${this.pageSize}`;
        if (this.lastEvaluatedKey) {
          url += `&startKey=${encodeURIComponent(
            JSON.stringify(this.lastEvaluatedKey)
          )}`;
        }
        // Add search criteria to the URL if they exist
        if (this.searchCriteria.name) {
          url += `&name=${encodeURIComponent(this.searchCriteria.name)}`;
        }
        if (this.searchCriteria.siren) {
          url += `&siren=${encodeURIComponent(this.searchCriteria.siren)}`;
        }
        if (this.searchCriteria.siret) {
          url += `&siret=${encodeURIComponent(this.searchCriteria.siret)}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (!this.companies) {
          this.companies = data.items;
        } else {
          this.companies = [...this.companies, ...data.items];
        }
        this.totalCount = data.Count;
        this.lastEvaluatedKey = data.LastEvaluatedKey;
        this.loading = false;
        window.scrollTo(0, document.body.scrollHeight);
      } catch (error) {
        console.error("Error fetching companies:", error);
      }
    },
    async fetchNextPage() {
      console.log("Fetching next page...");
      if (this.lastEvaluatedKey) {
        try {
          let url = `${this.apibaseUrl}/companies?pageSize=${this.pageSize}`;

          url += `&startKey=${encodeURIComponent(
            JSON.stringify(this.lastEvaluatedKey)
          )}`;

          const response = await fetch(url);
          const data = await response.json();

          const newCompanies = data.items.map((company) => ({
            id: company.id,
            name: company.name,
            location: company.location,
            industry: company.industry,
            description: company.description,
          }));

          this.companies = [...this.companies, ...newCompanies]; // Append new companies
          this.lastEvaluatedKey = data.LastEvaluatedKey;

          window.scrollTo(0, document.body.scrollHeight);
        } catch (error) {
          console.error("Error fetching next page:", error);
        }
      }
    },
    searchCompanies() {
      this.lastEvaluatedKey = null; // Reset pagination
      this.companies = null; // Clear previous results
      this.totalCount = 0; // Reset total count
      this.fetchCompanies(); // Fetch companies with the search criteria
    },
    goToCompanyDetails(companyId) {
      this.$router.push({ path: `/companies/${companyId}` });
    },
  },
};
</script>

<style scoped>
/* Styles for company cards remain unchanged */
.search-results {
  flex-wrap: wrap;
  flex-direction: column;
  gap: 20px; /* Increased gap for better spacing */
  max-width: 800px; /* Limit width for readability */
  margin: 20px auto; /* Center the cards */
}
</style>
