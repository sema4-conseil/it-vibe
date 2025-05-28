<template>
  <div v-if="loading">
    <p>Loading company details...</p>
    <div class="spinner"></div>
  </div>
  <div v-else-if="company">
    <div class="company-details-container">
      <div class="company-details">
        <h1 class="company-header">
          <span>{{ company.name }}</span>
        </h1>
        <div class="details-grid">
          <div class="detail-item">
            <strong>Country:</strong>
            <country-flag :country-code="company.country"> </country-flag>
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
            <strong>Siren:</strong> {{ company.siren }}
          </div>
          <div class="detail-item">
            <strong>Siret:</strong> {{ company.siret }}
          </div>
          <div class="detail-item">
            <strong>Creation Date:</strong>
            {{ formatDate(company.creationDate) }}
          </div>
        </div>
        <div v-if="company.president" class="president-details">
          <h2>President</h2>
          <p>
            <strong>Name:</strong> {{ company.president.firstname }}
            {{ company.president.lastname }}
          </p>
          <p><strong>Email:</strong> {{ company.president.email }}</p>
          <p><strong>Phone:</strong> {{ company.president.phoneNumber }}</p>
        </div>
      </div>
      <div class="company-reviews">
        <div
          v-if="company.metrics && company.metrics.review_count > 0"
          class="rating"
          :title="company.metrics.average_rating"
        >
          <h2>
            <span style="color: black"
              >Reviews ({{ company.metrics.review_count }})</span
            >
          </h2>
          <span v-for="n in Math.floor(company.metrics.average_rating)" :key="n"
            >★</span
          >
          <span
            v-for="n in 10 - Math.floor(company.metrics.average_rating)"
            :key="'empty-' + n"
            >☆</span
          >
        </div>
        <div class="reviews-scrollable">
          <div v-if="reviews && reviews.length > 0">
            <ReviewOverview
              v-for="review in reviews"
              :key="review.id"
              :review="review"
            />
          </div>
          <div v-else>
            <p>No reviews available.</p>
          </div>
          <transition name="fade-slide">
            <div id="reviewForm" v-if="showReviewForm" class="card">
              <textarea
                v-model="newReview.comment"
                placeholder="Write your review..."
                rows="4"
                @input="updateCommentLength"
              ></textarea>
              <p
                class="comment-feedback"
                :class="{ error: !isCommentValid && isSubmitted }"
              >
                {{ commentLengthMessage }}
              </p>
              <div class="form-grid">
                <div class="form-group">
                  <label for="rating">Rating:</label>
                  <select v-model="newReview.rating" id="rating" required>
                    <option value="" disabled selected>
                      Select your rating
                    </option>
                    <option v-for="rate in 10" :key="rate" :value="rate">
                      {{ rate }}
                    </option>
                  </select>
                  <p v-if="!newReview.rating && isSubmitted" class="error">
                    Rating is required.
                  </p>
                </div>
                <div class="form-group">
                  <label for="rating">Contract type:</label>
                  <select v-model="newReview.contractType" required>
                    <option value="" disabled selected>Contcat type</option>
                    <option value="CDI">CDI</option>
                    <option value="CDD">CDD</option>
                    <option value="INTERNSHIP">Internship</option>
                    <option value="CONTRACTOR">Contractor</option>
                    <option value="FREELANCE">Freelance</option>
                    <option value="OTHER">Other</option>
                  </select>
                  <p
                    v-if="!newReview.contractType && isSubmitted"
                    class="error"
                  >
                    Contract type is required.
                  </p>
                </div>
                <div class="form-group">
                  <label>Start date:</label>
                  <input type="date" v-model="newReview.startDate" required />
                  <p v-if="!newReview.startDate && isSubmitted" class="error">
                    Start date is required.
                  </p>
                </div>
                <div class="form-group">
                  <label>End date:</label>
                  <input type="date" v-model="newReview.endDate" />
                </div>
                <div>
                  <label class="checkbox-label">
                    <input
                      type="checkbox"
                      v-model="newReview.isAnonymous"
                      class="anonymous-checkbox"
                    />
                    Post anonymously
                  </label>
                </div>
              </div>
              <div class="button-container">
                <button @click="submitReview">Submit</button>
                <button @click="cancelReview" class="cancel">Cancel</button>
              </div>
            </div>
          </transition>
        </div>

        <div v-if="!showReviewForm">
          <button @click="toggleReviewForm">
            <i class="fas fa-plus"></i>Add
          </button>
        </div>
      </div>
    </div>
    <generic-modal
      v-if="this.modal.show"
      :isOpen="this.modal.show"
      @close="this.modal.show = false"
      ><div>
        <p>{{ modal.message }}</p>
      </div>
      <div v-if="modal.loading" class="spinner"></div>
    </generic-modal>
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
import GenericModal from "@/components/ui/GenericModal.vue";
import CountryFlag from "@/components/ui/CountyFlag.vue";
export default {
  props: ["id"],
  components: {
    ReviewOverview,
    GenericModal,
    // eslint-disable-next-line
    CountryFlag,
  },
  data() {
    return {
      company: null,
      loading: true,
      companyNotFound: false,
      apibaseUrl: process.env.VUE_APP_API_BASE_URL,
      reviews: [],
      showReviewForm: false,
      isSubmitted: false,
      newReview: {
        comment: "",
        isAnonymous: false,
        contractType: "",
        rating: null,
      },
      modal: {
        show: false,
        message: "",
        type: "",
        loading: false,
      },
    };
  },
  created() {
    this.fetchCompanyDetails();
  },
  computed: {
    isCommentValid() {
      const length = this.newReview.comment.length;
      return length >= 100 && length <= 1000;
    },
    commentLengthMessage() {
      const length = this.newReview.comment.length;
      if (length === 0) {
        return "Write your review (minimum 100 characters, maximum 1000 characters).";
      } else if (length < 100) {
        return `Minimum 100 characters required. Remaining: ${100 - length}`;
      } else if (length > 1000) {
        return `Maximum limit exceeded by ${length - 1000} characters.`;
      } else {
        return `Characters: ${length}/1000`;
      }
    },
  },
  methods: {
    updateCommentLength() {
      // Trigger computed properties to update in real-time
    },
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

        await this.fetchComapnyMetrics();
        this.loading = false;
      } catch (error) {
        this.loading = false;
      }
    },
    async fetchComapnyMetrics() {
      try {
        const response = await fetch(
          `${this.apibaseUrl}/companies/${this.id}/metrics`
        );
        if (!response.ok) {
          throw new Error("Failed to fetch company metrics.");
        }
        const data = await response.json();
        this.company.metrics = data;
      } catch (error) {
        console.error("Error fetching company metrics:", error);
      }
    },
    toggleReviewForm() {
      const token = localStorage.getItem("idToken");
      // Check if the user is logged in
      // If not, redirect to the login page
      if (!token) {
        let redirect_uri = this.$route.fullPath;
        this.$router.push(
          "/login?redirect_uri=" + encodeURIComponent(redirect_uri)
        );
      }
      this.showReviewForm = !this.showReviewForm;
      this.$nextTick(() => {
        if (this.showReviewForm) {
          const reviewForm = this.$el.querySelector("#reviewForm");
          if (reviewForm) {
            reviewForm.scrollIntoView({ behavior: "smooth" });
          }
        }
      });
    },
    cancelReview() {
      this.resetForm();
      this.showReviewForm = false;
    },
    resetForm() {
      this.newReview.comment = "";
      this.newReview.isAnonymous = false;
      this.newReview.rating = null;
      this.isSubmitted = false; // Reset the submitted state
    },
    async submitReview() {
      this.isSubmitted = true; // Set to true when the user tries to submit
      this.modal = {
        show: true, // Hide any previous modal messages
        message: "Sending review...",
        loading: true,
      };
      if (this.isCommentValid && this.newReview.rating) {
        try {
          // Retrieve the JWT token from session storage
          // TODO Change me
          const token = localStorage.getItem("idToken");
          const response = await fetch(`${this.apibaseUrl}/reviews/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              company_id: this.company.id,
              comment: this.newReview.comment,
              isAnonymous: this.newReview.isAnonymous,
              rating: this.newReview.rating,
              contractType: this.newReview.contractType,
              startDate: this.newReview.startDate,
              endDate: this.newReview.endDate || null,
            }),
          });
          this.modal = {
            show: false, // Hide any previous modal messages
            message: "",
            loading: false,
          };
          if (!response.ok) {
            if (response.status == 400) {
              this.modal.show = true;
              this.modal.message = await response
                .json()
                .then((data) => data.error || "Invalid review data.");
              return;
            }
          }
          await this.fetchCompanyDetails();
          await this.fetchComapnyMetrics();

          this.newReview.rating = null;
          this.newReview.contractType = "";
          this.newReview.startDate = "";
          this.newReview.endDate = "";
          this.isSubmitted = false; // Reset the submitted state
          this.newReview.comment = "";
          this.newReview.isAnonymous = false;
          this.showReviewForm = false;
        } catch (error) {
          this.modal.show = true;
          this.modal.message =
            "An error occurred while submitting your review.";
        }
      } else {
        this.modal.show = true;
        this.modal.message =
          "Please fix the errors in the form before submitting.";
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
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin: 15px 0;
}

.company-details-container {
  display: flex;
  margin: 0px auto;
  border-radius: 8px;
  height: calc(100vh - 60px);
}

.company-details {
  flex: 1; /* 2/3 of the container */
  padding: 20px;
  font-family: "Arial", sans-serif;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  margin-right: 10px; /* add some spacing between the two columns */
}

.company-reviews {
  flex: 2; /* 1/3 of the container */
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.company-header {
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  font-size: 1.5em;
  margin-bottom: 15px;
}

.company-header .metrics {
  font-weight: normal;
  font-size: 1em;
  margin-left: 10px;
  color: #555;
}

h2 {
  margin: 5px 0;
}

@media (max-width: 768px) {
  .company-details-container {
    flex-direction: column; /* Stack sections vertically */
  }

  .company-details {
    margin-right: 0; /* Remove spacing between sections */
    margin-bottom: 20px; /* Add spacing below the details section */
  }

  .company-reviews {
    flex: none; /* Adjust flex property */
  }
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
  display: flex;
  align-items: center;
  gap: 8px;
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
  flex: 1; /* Allow the reviews to take up available space */
}

.checkbox-label {
  display: flex;
  align-items: center;
}

.anonymous-checkbox {
  margin-right: 8px; /* Add spacing between the checkbox and the label text */
}
</style>
