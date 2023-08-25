import { createRouter, createWebHistory } from "vue-router";
import { blockUtilSetup, state } from "@/assets/script/global";
import { app } from "@/assets/script/allauth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "index",
      component: () => import("../views/IndexView.vue"),
      meta: {
        title: "Deeptrain",
      },
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue"),
      meta: {
        title: "Sign up | Deeptrain",
      },
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
      meta: {
        title: "Sign in | Deeptrain",
      },
    },
    {
      path: "/mail",
      name: "mail",
      component: () => import("../views/MailLoginView.vue"),
      meta: {
        title: "Sign in | Deeptrain",
      }
    },
    {
      path: "/verify",
      name: "verify",
      component: () => import("../views/VerifyView.vue"),
      meta: {
        title: "Verify | Deeptrain",
      },
    },
    {
      path: "/logout",
      name: "logout",
      component: () => import("../views/LogoutView.vue"),
      meta: {
        title: "Logout | Deeptrain",
      },
    },
    {
      path: "/forgot",
      name: "forgot",
      component: () => import("../views/ResetPassword.vue"),
      meta: {
        title: "Reset password | Deeptrain",
      },
    },
    {
      path: "/home",
      name: "home",
      component: () => import("../views/HomeView.vue"),
      children: [{
        path: "",
        name: "home_index",
        component: () => import("../views/home/GeneralView.vue"),
        meta: { title: "Home | Deeptrain" },
      }, {
        path: "oauth",
        name: "home_oauth",
        component: () => import("../views/home/OAuthView.vue"),
        meta: { title: "OAuth | Deeptrain" },
      }],
      meta: {
        title: "Home | Deeptrain",
      },
    },
    {
      path: "/oauth/github",
      name: "oauth_github",
      component: () => import("../views/oauth/GithubView.vue"),
      meta: {
        title: "Github OAuth | Deeptrain",
      },
    },
  ],
});

const auth_pages = ["/login", "/mail", "/register", "/forgot", "/oauth/github"];

router.beforeEach(async (to) => {
  await blockUtilSetup();
  if (auth_pages.includes(to.path)) app.guard();
  if (auth_pages.includes(to.path) && state.value === 1)
    return await router.push("/verify");
  if (auth_pages.includes(to.path) && state.value === 2)
    return await router.push("/home");
  if (to.path === "/logout" && state.value !== 2) return await router.push("/");
  if (to.path === "/verify" && state.value !== 1) return await router.push("/");
  if (to.path.startsWith("/home") && state.value !== 2) return await router.push("/");

  if (to.meta.title) document.title = to.meta.title as string;
});
export default router;
