import Vue from 'vue'
import Router from 'vue-router'
import TicketList from '@/components/TicketList'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'TicketList',
      component: TicketList
    }
  ]
})
