/* eslint-disable import/first */
import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

import createMutationsSharer from 'vuex-shared-mutations'

import Auth from './auth'

export default new Vuex.Store({
  plugins: [
    createMutationsSharer({ predicate: ['auth/login', 'auth/logout', 'auth/crLogin', 'auth/crLogout', 'auth/crPasswordSave'] })
  ],
  modules: {
    auth: Auth
  }
})
