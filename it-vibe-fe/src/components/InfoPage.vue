<template>
  <div>
    <div class="info-page">
      <h1>WEB</h1>
      <div>
        <span style="font-weight: bold">Version : </span>
        <span>{{ this.version }}</span>
      </div>
      <div>
        <span style="font-weight: bold">Env : </span>
        <span>{{ this.env }}</span>
      </div>
    </div>
    <div class="info-page">
      <h1>API</h1>
      <div>
        <span style="font-weight: bold">uri : </span>
        <span class="url">{{ this.baseUri }}</span>
        <div v-if="this.apiInfo">
          <div>
            <span style="font-weight: bold">Status : </span>
            <span class="up-status">{{ apiInfo.status }}</span>
          </div>
          <div>
            <span style="font-weight: bold">Version : </span>
            <span>{{ apiInfo.version }}</span>
          </div>
          <div>
            <span style="font-weight: bold">Env : </span>
            <span>{{ apiInfo.env }}</span>
          </div>
        </div>
        <div v-else>
          <span style="font-weight: bold; color: red"
            >No information about API, Contact your administrator</span
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "InfoPage",
  data() {
    return {
      env: process.env.VUE_APP_ENVIRONMENT,
      baseUri: process.env.VUE_APP_API_BASE_URL,
      version: process.env.VUE_APP_VERSION,
      apiInfo: null,
    };
  },
  mounted() {
    this.fetchHealthCheck();
  },
  methods: {
    fetchHealthCheck() {
      fetch(this.baseUri + "/healthcheck")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          this.apiInfo = data;
          console.log("API Info:", this.apiInfo);
        })
        .catch((error) => console.error("Error fetching version:", error));
    },
  },
};
</script>

<style scoped>
.info-page {
  padding: 20px;
  background-color: var(--card-background);
  border-radius: 8px;
  text-align: left;
  margin-bottom: 20px;
}
.info-page h1 {
  font-size: 24px;
  margin-bottom: 10px;
}
.info-page div {
  margin-bottom: 5px;
}
.info-page span {
  font-size: 16px;
}
.info-page span[style="font-weight: bold"] {
  font-weight: bold;
}
.info-page span[style="font-weight: bold"]::after {
  content: ": ";
}
.info-page span:not([style="font-weight: bold"]) {
  font-weight: normal;
}
.bold {
  font-weight: bold;
}
.up-status {
  background-color: green;
  color: white;
  padding: 2px;
  border-radius: 4px;
}
.down-status {
  color: red;
}

.url {
  color: blue;
  text-decoration: underline;
}

.version {
  font-weight: bold;
}
</style>
