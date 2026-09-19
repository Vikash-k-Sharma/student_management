import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../pages/Dashboard.vue'
import Students from '../pages/Students.vue'
import Courses from '../pages/Courses.vue'
import Reports from '../pages/Reports.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    component: Dashboard
  },
  {
    path: '/students',
    component: Students
  },
  {
    path: '/courses',
    component: Courses
  },
  {
    path: '/reports',
    component: Reports
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router