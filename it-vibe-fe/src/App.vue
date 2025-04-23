<template>
  <div id="app" class="app">
    <nav class="navbar">
      <ul class="menu">
        <li>
          <span>
            <router-link to="/">IT Vibes</router-link>
          </span>
        </li>
        <div class="right-menu">
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><a href="/join_us">Join us</a></li>
          <li v-if="connectedUser">
            <span><i class="fas fa-user"></i> {{ connectedUser }}</span>
          </li>
          <li v-if="connectedUser">
            <a href="/logout"><span>logout</span></a>
          </li>
          <li v-else>
            <a href="/login">Login</a>
          </li>
        </div>
      </ul>
    </nav>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import LoginPage from "./components/login/LoginPage.vue";

export default {
  name: "App",
  components: {
    // eslint-disable-next-line
    LoginPage,
  },
  data() {
    return {
      connectedUser: null, // Holds the username of the connected user
    };
  },
  mounted() {
    const idToken = sessionStorage.getItem("idToken");
    if (idToken) {
      try {
        // Decode the token (base64 decoding is required)
        const tokenPayload = JSON.parse(atob(idToken.split(".")[1])); // Extract payload
        this.connectedUser = tokenPayload["cognito:username"];
      } catch (error) {
        console.error("Failed to decode idToken", error);
      }
    }
  },
};
</script>

<style>
@import "@/assets/main.css";
.navbar {
  height: 50px;
}

.menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  margin-top: 0px;
  padding-inline-start: 0px;
}

.right-menu {
  display: flex;
  height: 100%;
  align-items: center;
}

.menu li a {
  color: white;
  text-decoration: none;
}

.menu li span {
  color: white;
  text-decoration: none;
}

.menu li a span {
  color: white;
  text-decoration: none;
}

.menu li {
  padding: 0 10px; /* Horizontal padding only */
  height: 100%;
  display: flex;
  align-items: center;
}

.menu li a {
  display: flex; /* Make links flex items */
  align-items: center; /* Vertically center link text */
  height: 100%; /* Make links occupy full height */
}
</style>
