import { createRouter, createWebHistory } from 'vue-router'
import { blockUtilSetup, state } from "@/assets/script/global";
import { app } from "@/assets/script/allauth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('../views/IndexView.vue'),
      meta: {
        title: 'Deeptrain',
      }
    }, {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: {
        title: 'Sign up | Deeptrain',
      }
    }, {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: 'Sign in | Deeptrain',
      }
    }, {
      path: '/verify',
      name: 'verify',
      component: () => import('../views/VerifyView.vue'),
      meta: {
        title: 'Verify | Deeptrain',
      }
    }, {
      path: '/logout',
      name: 'logout',
      component: () => import('../views/LogoutView.vue'),
      meta: {
        title: 'Logout | Deeptrain',
      }
    }, {
      path: '/forgot',
      name: 'forgot',
      component: () => import('../views/ResetPassword.vue'),
      meta: {
        title: 'Reset password | Deeptrain',
      }
    }
  ]
})

router.beforeEach(async (to) => {
  await blockUtilSetup();
  if (to.path === '/login') app.guard();
  if (["/login", "/register"].includes(to.path) && state.value === 1) return await router.push('/verify');
  if (["/login", "/register"].includes(to.path) && state.value === 2) return await router.push('/');
  if (to.path === '/logout' && state.value !== 2) return await router.push('/');
  if (to.path === '/verify' && state.value !== 1) return await router.push('/');
  // @ts-ignore
  if (to.meta.title) document.title = to.meta.title;
})
export default router
