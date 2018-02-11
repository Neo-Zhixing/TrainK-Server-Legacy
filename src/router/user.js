import Vue from 'vue'
import Router from 'vue-router'

import Account from '@/views/user/Account.vue'
import Security from '@/views/user/Security.vue'
import CR12306 from '@/views/user/CR12306.vue'
import Passenger from '@/views/user/Passenger.vue'
Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/user/setting',
  routes: [
    {
      path: '',
      redirect: '/account'
    },
    {
      path: '/account',
      name: 'Account',
      component: Account
    },
    {
      path: '/security',
      name: 'Security',
      component: Security
    },
    {
      path: '/12306',
      name: 'CR12306',
      component: CR12306
    },
    {
      path: '/passenger',
      name: 'Passenger',
      component: Passenger
    }
  ]
})
