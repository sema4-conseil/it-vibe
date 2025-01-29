import { createRouter, createWebHistory } from "vue-router";
import AboutPage from "../components/AboutPage.vue";

const routes = [
  {
    path: "/about",
    name: "About",
    component: AboutPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
