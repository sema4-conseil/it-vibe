<template>
  <div id="app">
    <nav class="navbar">
      <ul class="menu">
        <li>
          <span>
            <router-link to="/">IT Vibes</router-link>
          </span>
        </li>
        <div class="right-menu">
          <li><a href="#/about">About</a></li>
          <li><a href="#/contact">Contact</a></li>
          <li><a href="#/joint_us">Joint us</a></li>
        </div>
      </ul>
    </nav>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: "App",
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

.menu li {
  padding: 0 20px; /* Horizontal padding only */
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
