/* eslint-disable import/first */
import Vue from 'vue'
import Vuex, { mapState } from 'vuex'
Vue.use(Vuex)

import createMutationsSharer from 'vuex-shared-mutations'

import Auth from './auth'

export default new Vuex.Store({
  plugins: [
    createMutationsSharer({ predicate: [
      'auth/login',
      'auth/logout',
      'auth/crLogin',
      'auth/crLogout',
      'auth/crPasswordSave',
      'addMessage',
      'clearMessage'
    ]})
  ],
  state: {
    messages: []
  },
  mutations: {
    addMessage (state, message) { state.messages.push(message) },
    clearMessage (state) { state.messages = [] }
  },
  actions: {
    readMessages ({ commit, state }) {
      let messages = state.messages
      commit('clearMessage')
      return messages
    }
  },
  modules: {
    auth: Auth
  }
})

export const states = mapState(['messages'])
