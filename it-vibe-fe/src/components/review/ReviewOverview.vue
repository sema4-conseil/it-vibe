<template>
  <div class="card">
    <div class="card-header">
      <strong class="username">{{
        review.owner && !review.isAnonymous
          ? review.owner.username
          : "Anonymous"
      }}</strong>
      <div class="creation-date">{{ formattedDate }}</div>
    </div>

    <div class="rating" :title="'Rating: ' + review.rating">
      <span v-for="n in Math.floor(review.rating)" :key="n" class="star-filled"
        >★</span
      >
      <span
        v-for="n in 10 - Math.floor(review.rating)"
        :key="'empty-' + n"
        class="star-empty"
        >☆</span
      >
      <span class="rating-value">{{ review.rating.toFixed(1) }}</span>
    </div>

    <div class="review-details">
      <div class="detail-item">
        <label>Contract type:</label>
        <span>{{ review.contractType }}</span>
      </div>
      <div class="detail-item">
        <label>Start date:</label>
        <span>{{ review.startDate }}</span>
      </div>
      <div class="detail-item">
        <label>End date:</label>
        <span>{{ review.endDate ? review.endDate : "-" }}</span>
      </div>
    </div>

    <div class="comment-section">
      <p class="comment-text">{{ review.comment }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    review: {
      type: Object,
      required: true,
    },
  },
  computed: {
    formattedDate() {
      const date = new Date(this.review.creationDate);
      return date.toLocaleString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
};
</script>

<style scoped>
.card {
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: box-shadow 0.3s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.username {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.creation-date {
  font-size: 0.85rem;
  color: #666;
}

.rating {
  margin: 0.8rem 0;
  font-size: 1.2rem;
  line-height: 1;
}

.star-filled {
  color: #ffc107;
}

.star-empty {
  color: #ddd;
}

.rating-value {
  margin-left: 0.5rem;
  font-size: 0.9rem;
  color: #666;
  vertical-align: middle;
}

.review-details {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item label {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.2rem;
}

.detail-item span {
  font-weight: 500;
  color: #333;
}

.comment-section {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.comment-section label {
  font-size: 0.9rem;
  color: #666;
  display: block;
  margin-bottom: 0.5rem;
}

.comment-text {
  margin: 0;
  line-height: 1.6;
  color: #444;
  white-space: pre-line;
}

@media (max-width: 600px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }

  .review-details {
    grid-template-columns: 1fr;
  }
}
</style>
