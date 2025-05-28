<template>
  <div class="company-card">
    <div class="company-header">
      <h3>{{ company.name }}</h3>
      <span class="country-badge">{{ company.country }}</span>
    </div>
    <div class="company-details">
      <div class="detail-item">
        <span class="detail-label">Size</span>
        <span class="detail-value">{{
          company.size ? `${company.size} employees` : "N/A"
        }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Revenue</span>
        <span class="detail-value">{{ formatRevenue(company.revenue) }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Creation date</span>
        <span class="detail-value">{{ company.creationDate }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Siren</span>
        <span class="detail-value">{{ company.siren }}</span>
      </div>
      <div class="detail-item">
        <span class="detail-label">Siret</span>
        <span class="detail-value">{{ company.siret }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CompanyCard",
  props: {
    company: {
      type: Object,
      required: true,
      validator: (value) => {
        return value.name && value.country;
      },
    },
  },
  methods: {
    formatRevenue(revenue) {
      if (revenue === undefined || revenue === null) {
        return "N/A";
      }

      // Convert to number if it's a string
      const numRevenue =
        typeof revenue === "string" ? parseFloat(revenue) : revenue;

      if (isNaN(numRevenue)) {
        return "N/A";
      }

      if (numRevenue >= 1000000) {
        return `€${(numRevenue / 1000000).toFixed(1)}M`;
      } else if (numRevenue >= 1000) {
        return `€${(numRevenue / 1000).toFixed(1)}K`;
      }
      return `€${numRevenue.toFixed(0)}`;
    },
  },
};
</script>
<style scoped>
.company-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.company-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.company-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.company-header h3 {
  margin: 0;
  color: var(--navbar-background);
  font-size: 1.2rem;
}

.country-badge {
  background-color: var(--button-blue);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.company-details {
  display: flex;
  gap: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 0.8rem;
  color: #95a5a6;
  margin-bottom: 0.25rem;
}

.detail-value {
  font-weight: 500;
  color: var(--navbar-background);
}

@media (max-width: 600px) {
  .company-details {
    flex-direction: column;
    gap: 0.75rem;
  }
}
</style>
