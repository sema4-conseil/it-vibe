import { createRouter, createWebHashHistory } from "vue-router";
import AboutPage from "../components/AboutPage.vue";
import ContactPage from "@/components/ContactPage.vue";

const routes = [
  { path: "/about", component: AboutPage },
  { path: "/contact", component: ContactPage },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
