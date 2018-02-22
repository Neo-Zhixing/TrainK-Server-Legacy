/* eslint-disable import/first */
import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

import Ticket from './ticket'
import User from './user'
import MetroMap from './map'
import Trip from './trip'

export default new Router({
  mode: 'history',
  routes: [ Ticket, User, Trip, MetroMap ]
})
