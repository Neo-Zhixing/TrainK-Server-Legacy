/* eslint-disable import/first */
import Vue from 'vue'
Vue.config.productionTip = false

import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import VeeValidate from 'vee-validate'
Vue.use(VeeValidate)

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)

import 'bootstrap-vue/dist/bootstrap-vue.css'

import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'flatpickr/dist/themes/airbnb.css'

import './scss/index.scss'

import router from './router'
import store from './store'
import NavBar from './views/NavBar'
/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  components: { NavBar }
})
