<template>
  <div>
    <CreateCompany></CreateCompany>
    <patch-company></patch-company>
    <import-companies></import-companies>
  </div>
</template>
<script>
import CreateCompany from "./CreateCompany.vue";
import ImportCompanies from "./ImportCompanies.vue";
import PatchCompany from "./PatchCompany.vue";
export default {
  name: "ManageCompanies",
  components: {
    CreateCompany,
    PatchCompany,
    ImportCompanies,
  },
};
</script>
