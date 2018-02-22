import axios from '@/utils/axios'
import { mapState } from 'vuex'
export default {
  namespaced: true,
  state: {
    crAuthenticated: false,
    crPasswordSave: null,
    user: null
  },
  mutations: {
    crLogin (state) { state.crAuthenticated = true },
    crLogout (state) { state.crAuthenticated = false },
    crPasswordSave (state, data) { state.crPasswordSave = data },
    login (state, user) { state.user = user },
    logout (state) { state.user = null }
  },
  actions: {
    login ({ commit, state }, data) {
      data[data.credential.includes('@') ? 'email' : 'username'] = data.credential
      delete data.credential

      // Return user if already authenticated
      if (state.user !== null) return Promise.resolve(state.user)

      return axios.post('/user/session/', data) // Perform Login
      .then(() => axios.get('/user/'))          // Get user info
      .then(response => {
        commit('login', response.data)
        return response.data
      })
    },
    logout ({ commit, state }) {
      if (state.user === null) return Promise.resolve()
      return axios.delete('/user/session/')
      .then(() => {
        commit('logout')
      })
    },
    crCheckPasswordSave ({ commit, state }) {
      if (state.crPasswordSave) return Promise.resolve(state.crPasswordSave)
      return axios.get('/cr/user/')
      .then(response => {
        let data = { username: response.data.username, password: response.data.password_info }
        commit('crPasswordSave', data)
        return data
      })
      .catch(error => {
        if (error.response && error.response.status === 404) {
          commit('crPasswordSave', null)
          return
        }
        throw error
      })
    },
    crLogin ({ commit, state }, data) {
      let dataToSend = { captcha: data.captcha }
      if (!state.crPasswordSave.username) dataToSend.username = data.username
      if (!state.crPasswordSave.password) dataToSend.password = data.password
      return axios.post('/cr/user/session/', dataToSend)
      .then(response => {
        commit('crLogin')
      })
    },
    crCheckStatus ({ commit }) {
      return axios.get('/cr/user/session/')
      .then(() => {
        commit('crLogin')
        return true
      })
      .catch(error => {
        if (error.response && error.response.status === 403) {
          commit('crLogin')
          return false
        }
        throw error
      })
    }
  }
}
export const states = mapState('auth', ['user', 'crAuthenticated', 'crPasswordSave'])
