import { createRouter, createWebHistory } from 'vue-router'
import TicketView from '../views/TicketView.vue'
import TagView from '../views/TagView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'tickets',
      component: TicketView
    },
    {
      path: '/tags',
      name: 'tags',
      component: TagView
    }
  ]
})

export default router
