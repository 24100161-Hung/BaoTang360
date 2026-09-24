import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/tour/:slug',
    name: 'tour-view',
    component: () => import('@/views/TourView.vue'),
    props: true,
  },
  {
    path: '/tour-theme/:slug',
    name: 'theme-tour',
    component: () => import('@/views/ThemeTourView.vue'),
    props: true,
  },
  {
    path: '/collection',
    name: 'collection',
    component: () => import('@/views/CollectionView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
  },
  {
    path: '/admin/scenes',
    name: 'admin-scenes',
    component: () => import('@/views/admin/AdminSceneList.vue'),
    meta: { requiresAuth: true, role: 'admin' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

// Guard: Chặn truy cập nếu chưa đăng nhập
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('admin_token')

  if (to.meta.requiresAuth && !token) {
    next({
      name: 'login',
      query: { redirect: to.fullPath },
    })
  } else {
    next()
  }
})

export default router
