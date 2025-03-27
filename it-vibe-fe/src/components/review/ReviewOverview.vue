<template>
  <div class="review-overview">
    <strong>{{ review.author }}</strong>

    <div class="rating">
      <span v-for="n in review.rating" :key="n">★</span>
      <span v-for="n in 10 - review.rating" :key="'empty-' + n">☆</span>
    </div>
    {{ review.comment }}
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
};
</script>

<style scoped>
.review-overview {
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.rating {
  color: gold;
}
</style>
