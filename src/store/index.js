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
      'removeMessage',
      'clearMessage'
    ]})
  ],
  state: {
    messages: []
  },
  mutations: {
    addMessage (state, message) {
      if (!message.content) return false
      if (state.messages.some((item) => item.content === message.content)) return false
      if (!message.type) message.type = 'primary'
      if (message.time) message.timeRemaining = message.time
      state.messages.push(message)
      return true
    },
    removeMessage (state, message) { state.messages.splice(state.messages.indexOf(message), 1) },
    clearMessage (state) { state.messages = [] }
  },
  modules: {
    auth: Auth
  }
})

export const states = mapState(['messages'])
