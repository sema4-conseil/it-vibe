<template>
  <div class="card">
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
.rating {
  color: gold;
}
</style>
