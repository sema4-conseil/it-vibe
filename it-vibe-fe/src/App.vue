<template>
  <div id="app" class="app">
    <nav class="navbar">
      <ul class="menu">
        <li>
          <a href="/"
            ><span><i class="fa fa-home"></i>Home</span></a
          >
        </li>
        <li>
          <a href="/about"><i class="fa fa-info"></i>About</a>
        </li>
        <li>
          <a href="/contact"><i class="fa fa-envelope"></i>Contact</a>
        </li>
        <li>
          <a href="/join_us"><i class="fa fa-handshake"></i>Join us</a>
        </li>
        <li v-if="connectedUser">
          <span><i class="fas fa-user"></i> {{ connectedUser }}</span>
        </li>
        <li v-if="connectedUser">
          <a href="/logout"><i class="fa fa-sign-out-alt"></i>Logout</a>
        </li>
        <li v-else>
          <a href="/login"><i class="fas fa-sign-in-alt"></i>Login</a>
        </li>
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
  /* height: 50px; */
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--navbar-background);
  overflow: hidden;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

.menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  margin: 0px;
  padding-inline-start: 0px;
}

.menu-hidden {
  display: none !important; /* Hide the menu when toggled off */
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
.content {
  margin-top: 30px;
  padding: 0px 5px;
}

.fa,
.fas {
  margin: 0px 2px;
}

/* Media Query for small screens */
@media (max-width: 768px) {
  .menu {
    /* display: none; Hide menu by default */
    flex-direction: column; /* Stack the menu items */
    background-color: var(--navbar-background); /* Add a background color */
    position: unset;
    right: 0;
    width: 100%;
    z-index: 1200;
    padding-left: 2px;
  }
  .menu li {
    width: 100%; /* Make menu items take full width */
    text-align: center; /* Center text */
  }
  .content {
    margin-top: 160px;
    padding: 0px 5px;
  }
}
</style>
