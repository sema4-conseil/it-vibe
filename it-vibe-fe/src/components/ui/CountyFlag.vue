<template>
  <div>
    <span
      class="country-flag"
      :class="`fi fi-${countryCode.toLowerCase()}`"
      :title="countryName"
    ></span>
    <span>{{ countryName }}</span>
  </div>
</template>

<script>
export default {
  name: "CountryFlag",
  props: {
    countryCode: {
      type: String,
      required: true,
      validator: (value) => value.length === 2,
    },
  },
  computed: {
    countryName() {
      try {
        return new Intl.DisplayNames(["en"], { type: "region" }).of(
          this.countryCode.toUpperCase()
        );
      } catch {
        return this.countryCode;
      }
    },
  },
};
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/gh/lipis/flag-icons@6.6.6/css/flag-icons.min.css");

.country-flag {
  width: 1em;
  height: 1em;
  border: none;
  border-radius: 2px;
  margin: 0px 2px;
}
</style>
