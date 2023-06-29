import { createRouter, createWebHistory } from 'vue-router'
import { state } from "@/assets/script/global";

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
    },{
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: {
        title: 'Sign up | Deeptrain',
      }
    },{
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: 'Sign in | Deeptrain',
      }
    },{
      path: '/verify',
      name: 'verify',
      component: () => import('../views/VerifyView.vue'),
      meta: {
        title: 'Verify | Deeptrain',
      }
    }
  ]
})

router.beforeEach(async (to) => {
  if (["/login", "/register"].includes(to.path) && state.value === 1) return await router.push('/verify');
  if (["/login", "/register"].includes(to.path) && state.value === 2) return await router.push('/');
  if (to.path === '/verify' && state.value !== 1) return await router.push('/');
  // @ts-ignore
  if (to.meta.title) document.title = to.meta.title;
})
export default router
