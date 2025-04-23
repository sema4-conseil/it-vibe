import { createRouter, createWebHistory } from "vue-router";
import ContactPage from "@/components/ContactPage.vue";
import HomePage from "@/components/HomePage.vue";
import JoinUsPage from "@/components/JoinUsPage.vue";
import AboutPage from "@/components/AboutPage.vue";
import CompanyDetails from "@/components/company/CompanyDetails.vue";
import Login from "@/components/login/LoginPage.vue";
import CallBack from "@/components/login/CallBack.vue";
import LogoutPage from "@/components/login/LogoutPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/about", component: AboutPage },
  { path: "/contact", component: ContactPage },
  { path: "/join_us", component: JoinUsPage },
  {
    path: "/companies/:id",
    component: CompanyDetails,
    props: true, // Passe les paramètres de la route en tant que props au composant
  },
  { path: "/login", component: Login },
  { path: "/logout", component: LogoutPage },
  { path: "/callback", component: CallBack },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
