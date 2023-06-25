import { createRouter, createWebHistory } from 'vue-router'

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
    }
  ]
})

router.beforeEach((to) => {
  let title = to.meta.title; /** @ts-ignore **/
  title?document.title=title:undefined;
})
export default router
