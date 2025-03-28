<template>
  <div v-if="loading">
    <p>Loading company details...</p>
    <div class="spinner"></div>
  </div>
  <div v-else-if="company">
    <div class="company-details-container">
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
            <strong>Creation Date:</strong>
            {{ formatDate(company.creationDate) }}
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
      <div class="company-reviews">
        <h1>Reviews</h1>
        <div v-if="reviews && reviews.length > 0" class="reviews-scrollable">
          <ReviewOverview
            v-for="review in reviews"
            :key="review.id"
            :review="review"
          />
        </div>
        <div v-else>
          <p>No reviews available.</p>
        </div>
        <div>
          <button>Add Review</button>
        </div>
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
import ReviewOverview from "@/components/review/ReviewOverview.vue";

export default {
  props: ["id"],
  components: {
    ReviewOverview,
  },
  data() {
    return {
      company: null,
      loading: true,
      companyNotFound: false,
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
      reviews: [],
    };
  },
  created() {
    this.fetchCompanyDetails();
  },
  methods: {
    async fetchCompanyDetails() {
      try {
        let response = await fetch(`${this.apibaseUrl}/companies/${this.id}`);
        if (response.status === 404) {
          this.companyNotFound = true;
          this.loading = false;
          return;
        }
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        let data = await response.json();
        this.company = data;

        // Fetch reviews for the company
        let url = new URL(`${this.apibaseUrl}/reviews`);
        url.searchParams.append("companyId", this.company.id);
        response = await fetch(url);
        data = await response.json();
        this.reviews = data;

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
.company-details-container {
  display: flex;
  margin: 20px auto;
  border-radius: 8px;
}

.company-details {
  flex: 2; /* 2/3 of the container */
  padding: 20px;
  font-family: "Arial", sans-serif;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-right: 10px; /* add some spacing between the two columns */
}

.company-reviews {
  flex: 1; /* 1/3 of the container */
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.detail-item {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
}

.president-details,
.description {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.reviews-scrollable {
  overflow-y: auto;
  max-height: 620px;
  flex: 1; /* Allow the reviews to take up available space */
}

button {
  width: 25%;
}
</style>
