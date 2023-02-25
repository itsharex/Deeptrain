import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('../views/index.vue'),
      meta: {
        title: 'Zh-Website',
      }
    },{
      path: '/register',
      name: 'register',
      component: () => import('../views/register.vue'),
      meta: {
        title: 'Sign up | Zh-Website',
      }
    },{
      path: '/login',
      name: 'login',
      component: () => import('../views/login.vue'),
      meta: {
        title: 'Sign in | Zh-Website',
      }
    }
  ]
})

router.beforeEach((to) => {
  let title = to.meta.title; /** @ts-ignore **/
  title?document.title=title:undefined;
})
export default router
