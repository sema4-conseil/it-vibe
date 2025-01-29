import { createRouter, createWebHashHistory } from "vue-router";
import AboutPage from "../components/AboutPage.vue";

const routes = [{ path: "/about", component: AboutPage }];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
