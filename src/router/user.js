import Vue from 'vue'
import Router from 'vue-router'

import Account from '@/views/user/Account.vue'
import Security from '@/views/user/Security.vue'
Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/user/setting',
  routes: [
    {
      path: '/',
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
    }
  ]
})
