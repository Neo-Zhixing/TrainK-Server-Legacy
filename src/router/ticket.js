import Vue from 'vue'
import Router from 'vue-router'
import TicketHome from '@/views/ticket/Home'
import TicketList from '@/views/ticket/List'

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
    }
  ]
})
