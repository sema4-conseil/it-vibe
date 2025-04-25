<template>
  <div>
    <!-- Search Panel -->
    <div class="search-container">
      <form @submit.prevent="searchCompanies" class="search-form">
        <div class="form-group">
          <label for="name">Name</label>
          <input placeholder="Name" id="name" v-model="searchCriteria.name" />
        </div>
        <div class="form-group">
          <label for="siren">SIREN</label>
          <input type="text" id="siren" v-model="searchCriteria.siren" />
        </div>
        <div class="form-group">
          <label for="siret">SIRET</label>
          <input type="text" id="siret" v-model="searchCriteria.siret" />
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
    <div v-else-if="companies" class="company-cards">
      <div
        v-for="company in companies"
        :key="company.id"
        class="company-card"
        @click="goToCompanyDetails(company.id)"
      >
        <h2>{{ company.name }}</h2>
        <p><strong>Location:</strong> {{ company.location }}</p>
        <p><strong>Industry:</strong> {{ company.industry }}</p>
      </div>
      <div>
        <button @click="fetchNextPage()" :disabled="!lastEvaluatedKey">
          <i class="fa fa-forward"></i>Next Items
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      companies: [],
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
      lastEvaluatedKey: null,
      pageSize: 4,
      loading: false,
      searchCriteria: {
        name: "",
        siren: "",
        siret: "",
      },
    };
  },
  methods: {
    async fetchCompanies(startKey) {
      try {
        this.loading = true;
        let url = `${this.apibaseUrl}/companies?pageSize=${this.pageSize}`;
        if (startKey) {
          url += `&startKey=${encodeURIComponent(JSON.stringify(startKey))}`;
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

        this.companies = data.items.map((company) => ({
          id: company.id,
          name: company.name,
          location: company.location,
          industry: company.industry,
          description: company.description,
        }));
        this.lastEvaluatedKey = data.LastEvaluatedKey;
        this.loading = false;
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
.company-cards {
  padding: 20px; /* Increased padding to match content */
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  gap: 20px; /* Increased gap for better spacing */
  max-width: 800px; /* Limit width for readability */
  margin: 20px auto; /* Center the cards */
}

.company-card {
  border: 1px solid #e0e0e0; /* Lighter border to match overall style */
  border-radius: 12px; /* Slightly more rounded corners */
  width: 100%;
  background-color: white; /* White background for cards */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* Subtle shadow */
  padding: 10px; /* Padding inside the cards */
  transition: box-shadow 0.3s ease; /* Smooth shadow transition */
}

.company-card:hover {
  border: 1px solid var(--button-blue);
  cursor: pointer;
}

.company-card h2 {
  font-size: 1.5em;
  margin-bottom: 5px;
  color: #333;
}

.company-card p {
  font-size: 1em;
  color: #555;
  margin-bottom: 8px;
}

.company-card strong {
  font-weight: 600;
  color: #333;
}
</style>
