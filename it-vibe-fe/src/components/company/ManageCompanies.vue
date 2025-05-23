<template>
  <div>
    <CreateCompany></CreateCompany>
    <patch-company></patch-company>
  </div>
</template>
<script>
import CreateCompany from "./CreateCompany.vue";
import PatchCompany from "./PatchCompany.vue";
export default {
  name: "ManageCompanies",
  components: {
    CreateCompany,
    PatchCompany,
  },
};
</script>
