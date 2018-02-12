/* eslint-disable import/first */
import Vue from 'vue'
Vue.config.productionTip = false

import Vuex, { mapState } from 'vuex'
Vue.use(Vuex)

import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import VeeValidate from 'vee-validate'
Vue.use(VeeValidate)

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)

import axios from '@/utils/axios'

export default Vue

export const store = new Vuex.Store({
  state: {
    crAuthenticated: false,
    user: null
  },
  mutations: {
    crLogin (state) { state.crAuthenticated = true },
    crLogout (state) { state.crAuthenticated = false },
    login (state, user) { state.user = user },
    logout (state) { state.user = null }
  },
  actions: {
    login ({ commit, state }, data) {
      data[data.credential.includes('@') ? 'email' : 'username'] = data.credential
      delete data.credential

      // Return user if already authenticated
      if (state.user !== null) return new Promise((resolve) => { resolve(state.user) })

      return axios.post('/user/session/', data) // Perform Login
      .then(() => axios.get('/user/'))          // Get user info
      .then(response => {
        commit('login', response.data)
        return new Promise((resolve) => { resolve(response.data) })
      })
    },
    logout ({ commit, state }) {
      if (state.user === null) return new Promise((resolve) => { resolve() })
      return axios.delete('/user/session/')
      .then(() => {
        commit('logout')
        return new Promise((resolve) => { resolve() })
      })
    }
  }
})

export const authStates = mapState(['user'])
