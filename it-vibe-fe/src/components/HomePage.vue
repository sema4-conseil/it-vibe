<template>
  <div>
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
      <button @click="fetchNextPage()" :disabled="!lastEvaluatedKey">
        Next Items
      </button>
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
      loading: true,
    };
  },
  created() {
    this.fetchCompanies();
  },
  methods: {
    async fetchCompanies(startKey) {
      try {
        let url = `${this.apibaseUrl}/companies?pageSize=${this.pageSize}`;
        if (startKey) {
          url += `&startKey=${encodeURIComponent(JSON.stringify(startKey))}`;
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
    goToCompanyDetails(companyId) {
      this.$router.push({ path: `/companies/${companyId}` });
    },
  },
};
</script>

<style>
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
  box-shadow: 0 4px 8px rgb(19, 0, 0); /* Slightly larger shadow on hover */
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
button {
  width: 20%;
}
</style>
