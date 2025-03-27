<template>
  <div v-if="company" class="company-details">
    <h1>{{ company.name }}</h1>
    <div class="details-grid">
      <div class="detail-item">
        <strong>Location:</strong> {{ company.location }}, {{ company.country }}
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
  <div v-else>
    <p>Loading company details...</p>
  </div>
</template>
<script>
export default {
  props: ["id"],
  data() {
    return {
      company: null,
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
        const data = await response.json();
        this.company = data;
      } catch (error) {
        console.error("Error fetching company details:", error);
      }
    },
    formatRevenue(revenue) {
      return Number(revenue).toLocaleString(); // Formatta il fatturato con separatori di migliaia
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString(); // Formatta la data in un formato leggibile
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
