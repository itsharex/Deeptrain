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

router.beforeEach(async (to) => {  // @ts-ignore
  if (to.meta.title) document.title = to.meta.title;
  if (to.path in ["/login", "/register"] && state.value === 1) await router.push('/verify');
  if (to.path in ["/login", "/register"] && state.value === 2) await router.push('/');
  if (to.path === '/verify' && state.value !== 1) await router.push('/');
})
export default router
