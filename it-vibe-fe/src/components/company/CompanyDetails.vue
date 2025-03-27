<template>
  <div v-if="loading">
    <p>Loading company details...</p>
    <div class="spinner"></div>
  </div>
  <div v-else-if="company">
    <div class="company-details">
      <h1>{{ company.name }}</h1>
      <div class="details-grid">
        <div class="detail-item">
          <strong>Location:</strong> {{ company.location }},
          {{ company.country }}
        </div>
        <div class="detail-item">
          <strong>Industry:</strong> {{ company.industry }}
        </div>
        <div class="detail-item">
          <strong>Size:</strong> {{ company.size }} employees
        </div>
        <div class="detail-item">
          <strong>Revenue:</strong> ${{ formatRevenue(company.revenue) }}
        </div>
        <div class="detail-item">
          <strong>Address:</strong> {{ company.adress }}
        </div>
        <div class="detail-item">
          <strong>Creation Date:</strong> {{ formatDate(company.creationDate) }}
        </div>
      </div>
      <div class="president-details">
        <h2>President</h2>
        <p>
          <strong>Name:</strong> {{ company.president.firstname }}
          {{ company.president.lastname }}
        </p>
        <p><strong>Email:</strong> {{ company.president.email }}</p>
        <p><strong>Phone:</strong> {{ company.president.phoneNumber }}</p>
      </div>
      <div class="description">
        <h2>Description</h2>
        <p>{{ company.description }}</p>
      </div>
    </div>
  </div>
  <div v-else-if="companyNotFound">
    <h2>Company unknown.</h2>
  </div>
  <div v-else>
    <p>An error occurred while loading company details.</p>
  </div>
</template>

<script>
export default {
  props: ["id"],
  data() {
    return {
      company: null,
      loading: true,
      companyNotFound: false,
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
    };
  },
  created() {
    this.fetchCompanyDetails();
  },
  methods: {
    async fetchCompanyDetails() {
      try {
        const response = await fetch(`${this.apibaseUrl}/companies/${this.id}`);
        if (response.status === 404) {
          this.companyNotFound = true;
          this.loading = false;
          return;
        }
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.company = data;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching company details:", error);
        this.loading = false;
      }
    },
    formatRevenue(revenue) {
      return Number(revenue).toLocaleString();
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },
  },
};
</script>

<style scoped>
.company-details {
  padding: 20px;
  font-family: "Arial", sans-serif;
  max-width: 800px;
  margin: 20px auto;
  border-radius: 8px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.detail-item {
  background-color: white;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.president-details,
.description {
  background-color: white;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}
</style>
