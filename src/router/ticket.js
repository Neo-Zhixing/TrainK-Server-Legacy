import Vue from 'vue'
import Router from 'vue-router'
import TicketHome from '@/views/ticket/Home'
import TicketList from '@/views/ticket/List'
import Order from '@/views/ticket/Order'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/ticket',
  routes: [
    {
      path: '/',
      name: 'TicketHome',
      component: TicketHome
    },
    {
      path: '/list',
      name: 'TicketList',
      component: TicketList
    },
    {
      path: '/order',
      name: 'PlaceOrders',
      component: Order
    }
  ]
})
