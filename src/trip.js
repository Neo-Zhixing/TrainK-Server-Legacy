// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable import/first */
import Vue from 'vue'
Vue.config.productionTip = false

import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import VeeValidate from 'vee-validate'
Vue.use(VeeValidate)

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)

import App from '@/views/trip/App'
import router from '@/router/trip'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
