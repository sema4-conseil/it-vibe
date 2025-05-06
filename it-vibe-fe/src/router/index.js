import { createRouter, createWebHistory } from "vue-router";
import { jwtDecode } from "jwt-decode";
import ContactPage from "@/components/contact/ContactPage.vue";
import HomePage from "@/components/HomePage.vue";
import JoinUsPage from "@/components/JoinUsPage.vue";
import AboutPage from "@/components/AboutPage.vue";
import CompanyDetails from "@/components/company/CompanyDetails.vue";
import Login from "@/components/login/LoginPage.vue";
import CallBack from "@/components/login/CallBack.vue";
import LogoutPage from "@/components/login/LogoutPage.vue";
import ManageCompanies from "@/components/company/ManageCompanies.vue";
import NotAuthorizedPage from "@/components/login/NotAuthorizedPage.vue";
import ManageContactMessages from "@/components/contact/ManageContactMessages.vue";

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
  {
    path: "/manage_companies",
    component: ManageCompanies,
    meta: { requiresAdmin: true },
  },
  {
    path: "/manage_contact_messages",
    component: ManageContactMessages,
    meta: { requiresAdmin: true },
  },
  {
    path: "/not-authorized",
    name: "NotAuthorized",
    component: NotAuthorizedPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  // Check if the route requires admin rights
  if (to.matched.some((record) => record.meta.requiresAdmin)) {
    const token = sessionStorage.getItem("idToken");
    if (token) {
      try {
        const decodedToken = jwtDecode(token); // Decode the JWT
        const userGroups = decodedToken["cognito:groups"] || [];

        // Check if the user belongs to the 'admin' group
        if (userGroups.includes("admin")) {
          next(); // Allow access
        } else {
          next({ name: "NotAuthorized" }); // Redirect to 'Not Authorized' page
        }
      } catch (error) {
        console.error("Invalid token:", error);
        next({ name: "NotAuthorized" }); // Redirect on error
      }
    } else {
      next({ name: "NotAuthorized" }); // Redirect if no token is found
    }
  } else {
    next(); // Proceed if no restrictions
  }
});

export default router;
