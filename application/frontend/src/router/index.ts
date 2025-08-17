import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: {
      title: 'Accueil - Todo List',
      description: 'Tableau de bord de votre gestionnaire de tâches',
    },
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: () => import('@/views/TasksView.vue'),
    meta: {
      title: 'Tâches - Todo List',
      description: 'Gérez vos tâches efficacement',
    },
  },
  {
    path: '/categories',
    name: 'categories',
    component: () => import('@/views/CategorieView.vue'),
    meta: {
      title: 'Categories - Todo List',
      description: 'Gérez vos categories efficacement',
    },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue'),
    meta: {
      title: 'À propos - Todo List',
      description: "En savoir plus sur l'application",
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
    meta: {
      title: 'Page non trouvée - Todo List',
    },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    return savedPosition || { top: 0 }
  },
})

function updateMeta(to: any) {
  if (to.meta.title) {
    document.title = to.meta.title as string
  }

  if (to.meta.description) {
    let metaDescription = document.querySelector('meta[name="description"]')
    if (!metaDescription) {
      metaDescription = document.createElement('meta')
      metaDescription.setAttribute('name', 'description')
      document.head.appendChild(metaDescription)
    }
    metaDescription.setAttribute('content', to.meta.description as string)
  }
}

router.beforeEach((to, _from, next) => {
  updateMeta(to)
  next()
})

export default router
