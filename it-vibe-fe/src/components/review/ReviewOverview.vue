<template>
  <div class="card">
    <strong>{{ review.owner.user_id || "Anonymous" }}</strong>
    <div class="creation-date">{{ formattedDate }}</div>

    <div class="rating" :title="review.rating">
      <span v-for="n in Math.floor(review.rating)" :key="n">★</span>
      <span v-for="n in 10 - Math.floor(review.rating)" :key="'empty-' + n"
        >☆</span
      >
    </div>
    <p>{{ review.comment }}</p>
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
        second: "2-digit",
        timeZoneName: "short",
      });
    },
  },
};
</script>

<style scoped>
.strong {
  font-size: 1.2em;
}

.creation-date {
  font-size: 0.9em;
  color: #888;
  margin-bottom: 0.5rem;
}

.rating {
  color: gold;
  display: inline-block;
  margin-bottom: 0.5rem;
}

.rating span {
  cursor: default;
}
</style>
