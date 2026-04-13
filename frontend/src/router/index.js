/**
 * 路由配置
 * 未登录访问受保护路由时，自动重定向到登录页
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/LoginPage.vue'),
    meta: { requiresAuth: false, title: '登录 - 芯智云匠' }
  },
  {
    path: '/',
    component: () => import('@/components/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/demo'
      },
      {
        path: 'demo',
        name: 'Demo',
        component: () => import('@/views/demo/DemoPage.vue'),
        meta: { title: 'AI 能力演示 - 芯智云匠', requiresAuth: true }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/demo'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录强制跳转登录页
router.beforeEach((to) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.name === 'Login' && userStore.isLoggedIn) {
    return { path: '/demo' }
  }
  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
