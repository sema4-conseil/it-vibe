<template>
  <div class="company-cards">
    <div v-for="company in companies" :key="company.id" class="company-card">
      <h2>{{ company.name }}</h2>
      <p><strong>Location:</strong> {{ company.location }}</p>
      <p><strong>Industry:</strong> {{ company.industry }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      companies: [],
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
    };
  },
  created() {
    this.fetchCompanies();
  },
  methods: {
    async fetchCompanies() {
      try {
        const response = await fetch(`${this.apibaseUrl}/companies`);
        const data = await response.json();
        this.companies = data.map((company) => ({
          id: company.id,
          name: company.name,
          location: company.location,
          industry: company.industry,
          description: company.description,
        }));
      } catch (error) {
        console.error("Error fetching companies:", error);
      }
    },
  },
};
</script>

<style>
.company-cards {
  padding: 5px;
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  gap: 16px;
}

.company-card {
  border: 1px solid #1c1c1c;
  border-radius: 8px;
  width: 100%;
}
</style>
