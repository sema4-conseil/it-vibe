<template>
  <div id="app">
    <nav class="navbar">
      <ul class="menu">
        <li class="logo">IT Vibes</li>
        <li><a href="/">Home</a></li>
        <li><a href="#/about">About</a></li>
        <li><a href="#/contact">Contact</a></li>
        <li><a href="#/joint_us">Joint us</a></li>
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
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
  color: #333;
  overflow-x: hidden; /* Prevent horizontal scroll */
}

#app {
  text-align: center;
}

.navbar {
  background-color: #333;
  overflow: hidden;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000; /* Ensure the navbar is above other content */
}

.menu {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
}

.menu li {
  padding: 14px 20px;
}

.menu li a {
  color: white;
  text-decoration: none;
  display: block;
}

.menu li a:hover {
  background-color: #575757;
}

.menu li.logo {
  flex-grow: 1;
  text-align: left;
  padding-left: 20px;
  color: white;
}

.content {
  margin-top: 60px; /* Add margin to avoid content being hidden behind the fixed navbar */
  overflow-y: auto;
  height: calc(100vh - 60px); /* Adjust height to be scrollable */
}

.search-container {
  margin-top: 50px;
}

.search-bar {
  padding: 10px;
  width: 50%;
  max-width: 500px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-bar:focus {
  outline: none;
  border-color: #333;
}
</style>
