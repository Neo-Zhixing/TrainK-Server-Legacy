/* eslint-disable import/first */
import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

import Ticket from './ticket'

export default new Router({
  mode: 'history',
  routes: [
    Ticket
  ]
})
