import { createRouter, createWebHashHistory } from "vue-router";
import ContactPage from "@/components/ContactPage.vue";
import HomePage from "@/components/HomePage.vue";
import JoinUsPage from "@/components/JoinUsPage.vue";
import AboutPage from "@/components/AboutPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/about", component: AboutPage },
  { path: "/contact", component: ContactPage },
  { path: "/joint_us", component: JoinUsPage },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
