import { createRouter, createWebHistory } from "vue-router";
import { blockUtilSetup, state } from "@/assets/script/global";
import { app } from "@/assets/script/allauth";
import IndexView from "@/views/IndexView.vue";
import LoginView from "@/views/LoginView.vue";
import MailLoginView from "@/views/MailLoginView.vue";
import VerifyView from "@/views/VerifyView.vue";
import LogoutView from "@/views/LogoutView.vue";
import ResetPassword from "@/views/ResetPassword.vue";
import RegisterView from "@/views/RegisterView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "index",
      component: IndexView,
      meta: {
        title: "Deeptrain",
      },
    },
    {
      path: "/service",
      name: "service",
      component: () => import("../views/ServiceView.vue"),
      meta: {
        title: "Terms of Service | Deeptrain",
      },
    },
    {
      path: "/privacy",
      name: "privacy",
      component: () => import("../views/PrivacyView.vue"),
      meta: {
        title: "Privacy Policy | Deeptrain",
      },
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      meta: {
        title: "Sign up | Deeptrain",
      },
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: {
        title: "Sign in | Deeptrain",
      },
    },
    {
      path: "/mail",
      name: "mail",
      component: MailLoginView,
      meta: {
        title: "Sign in | Deeptrain",
      },
    },
    {
      path: "/verify",
      name: "verify",
      component: VerifyView,
      meta: {
        title: "Verify | Deeptrain",
      },
    },
    {
      path: "/logout",
      name: "logout",
      component: LogoutView,
      meta: {
        title: "Logout | Deeptrain",
      },
    },
    {
      path: "/forgot",
      name: "forgot",
      component: ResetPassword,
      meta: {
        title: "Reset password | Deeptrain",
      },
    },
    {
      path: "/home",
      name: "home",
      component: () => import("../views/HomeView.vue"),
      children: [
        {
          path: "",
          name: "home_index",
          component: () => import("../views/home/GeneralView.vue"),
          meta: { title: "Home | Deeptrain" },
        },
        {
          path: "auth",
          name: "home_auth",
          component: () => import("../views/home/AuthView.vue"),
          meta: { title: "Auth | Deeptrain" },
        },
        {
          path: "oauth",
          name: "home_oauth",
          component: () => import("../views/home/OAuthView.vue"),
          meta: { title: "OAuth | Deeptrain" },
        },
        {
          path: "wallet",
          name: "home_wallet",
          component: () => import("../views/home/WalletView.vue"),
          meta: { title: "Wallet | Deeptrain" },
        },
        {
          path: "package",
          name: "home_package",
          component: () => import("../views/home/PackageView.vue"),
          meta: { title: "Package | Deeptrain" },
        },
      ],
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
    {
      path: "/oauth/google",
      name: "oauth_google",
      component: () => import("../views/oauth/GoogleView.vue"),
      meta: {
        title: "Google OAuth | Deeptrain",
      },
    },
    {
      path: "/pay/wechat/order",
      name: "pay_wechat_order",
      component: () => import("../views/pay/WechatPaymentView.vue"),
      meta: {
        title: "Wechat Order | Deeptrain",
      },
    },
    {
      path: "/pay/alipay/return",
      name: "pay_alipay_return",
      component: () => import("../views/pay/AlipayCallbackView.vue"),
      meta: {
        title: "Alipay Trade | Deeptrain",
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
  if (
    auth_pages.includes(to.path) &&
    !to.path.startsWith("/oauth") &&
    state.value === 2
  )
    return await router.push("/home");
  if (to.path === "/logout" && state.value !== 2) return await router.push("/");
  if (to.path === "/verify" && state.value !== 1) return await router.push("/");
  if (to.path.startsWith("/home") && state.value !== 2)
    return await router.push("/");

  if (to.meta.title) document.title = to.meta.title as string;
});
export default router;
