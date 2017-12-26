import Vue from 'vue'
import Router from 'vue-router'

import Account from '@/views/user/Account.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/user',
  routes: [
    {
      path: '/',
      redirect: '/settings/account'
    },
    {
      path: '/settings',
      redirect: '/settings/account'
    },
    {
      path: '/settings/account',
      name: 'Account',
      component: Account
    }
  ]
})
