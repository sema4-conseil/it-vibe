<template>
  <div id="app" class="app">
    <nav class="navbar">
      <!-- fa-hamburger -->
      <ul v-if="this.isCollapsed" class="menu">
        <li @click="expandMenu()">
          <a>
            <span><i class="fa fa-bars"></i></span>
          </a>
        </li>
      </ul>
      <ul v-else class="menu">
        <!-- Left-aligned items -->
        <li>
          <a href="/"
            ><span><i class="fa fa-home"></i>IT-Vibe</span></a
          >
        </li>
        <li>
          <a href="/about"><i class="fa fa-info"></i>About</a>
        </li>
        <li>
          <a href="/contact"><i class="fa fa-envelope"></i>Contact</a>
        </li>
        <!-- <li>
          <a href="/join_us"><i class="fa fa-handshake"></i>Join us</a>
        </li> -->
        <li v-if="isAdmin" class="admin-menu">
          <a href="/manage_companies"
            ><i class="fa fa-cog"></i>Manage companies</a
          >
        </li>
        <li v-if="isAdmin" class="admin-menu">
          <a href="/manage_contact_messages"
            ><i class="fa fa-cog"></i>Manage contact messages</a
          >
        </li>

        <!-- Right-aligned items -->
        <div class="menu-right">
          <li v-if="connectedUser">
            <span><i class="fas fa-user"></i> {{ connectedUser }}</span>
          </li>
          <li>
            <router-link to="/info">
              <i class="fa fa-info-circle">Info</i></router-link
            >
          </li>
          <li v-if="connectedUser">
            <a href="/logout"><i class="fa fa-sign-out-alt"></i>Logout</a>
          </li>
          <li v-else>
            <a href="/login"><i class="fas fa-sign-in-alt"></i>Login</a>
          </li>
        </div>
      </ul>
    </nav>
    <div id="content" @click="collapseMenu()" class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import LoginPage from "./components/login/LoginPage.vue";
const maxWidth = 768;
export default {
  name: "App",
  components: {
    // eslint-disable-next-line
    LoginPage,
  },
  data() {
    return {
      connectedUser: null,
      isAdmin: false,
      isCollapsed: false,
    };
  },
  mounted() {
    //eslint-disable-next-line
    window.addEventListener("resize", () => {
      this.isCollapsed = window.innerWidth <= maxWidth;
    });
    const idToken = localStorage.getItem("idToken");
    if (idToken) {
      try {
        const tokenPayload = JSON.parse(atob(idToken.split(".")[1]));
        this.connectedUser = tokenPayload["cognito:username"];
        const userGroups = tokenPayload["cognito:groups"] || [];
        this.isAdmin = userGroups.includes("admin");
      } catch (error) {
        console.error("Failed to decode idToken", error);
      }
    }
    // Check if the screen width is less than or equal to 768px
    // and collapse the menu if it is
    this.isCollapsed = window.innerWidth <= maxWidth;
  },
  methods: {
    collapseMenu() {
      this.isCollapsed = window.innerWidth <= maxWidth;
    },
    expandMenu() {
      this.isCollapsed = false;
    },
  },
};
</script>

<style>
@import "@/assets/main.css";

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--navbar-background);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.menu {
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0;
  list-style: none;
  width: 100%;
}

.menu li {
  padding: 0 10px;
  height: 100%;
  display: flex;
  align-items: center;
}

.menu li a,
.menu li span {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  height: 100%;
}

.menu-right {
  margin-left: auto; /* Push the right menu to the end */
  display: flex;
  align-items: center;
}

.content {
  margin-top: 30px;
  padding: 0 5px;
  height: calc(100vh - 60px); /* Full viewport height minus navbar */
  overflow-y: auto; /* Scrollbar only on content */
}

.admin-menu {
  background-color: var(--button-orange);
  margin: 2px 2px;
}

.fa,
.fas {
  margin: 0 2px;
}

/* Media Query for small screens */
@media (max-width: 768px) {
  .menu {
    flex-direction: column;
    background-color: var(--navbar-background);
    position: unset;
    width: 100%;
    z-index: 1200;
  }

  .menu li {
    width: 100%;
    text-align: center;
  }

  .menu-right {
    flex-direction: column;
    background-color: var(--navbar-background);
    position: unset;
    width: 100%;
    z-index: 1200;
  }
}
</style>
