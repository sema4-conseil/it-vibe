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
@import "@/assets/main.css";
</style>
