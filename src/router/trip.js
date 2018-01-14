import Vue from 'vue'
import Router from 'vue-router'

import List from '@/views/trip/List.vue'
Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/trip',
  routes: [
    {
      path: '',
      name: 'TripList',
      component: List
    }
  ]
})
