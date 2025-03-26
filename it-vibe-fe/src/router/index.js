import { createRouter, createWebHashHistory } from "vue-router";
import ContactPage from "@/components/ContactPage.vue";
import HomePage from "@/components/HomePage.vue";
import JoinUsPage from "@/components/JoinUsPage.vue";
import AboutPage from "@/components/AboutPage.vue";
import CompanyDetails from "@/components/company/CompanyDetails.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/about", component: AboutPage },
  { path: "/contact", component: ContactPage },
  { path: "/joint_us", component: JoinUsPage },
  {
    path: "/companies/:id",
    component: CompanyDetails,
    props: true, // Passe les paramètres de la route en tant que props au composant
  },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
