// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable import/first */
import Vue from 'vue'
Vue.config.productionTip = false

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)

import 'bootstrap-vue/dist/bootstrap-vue.css'
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'flatpickr/dist/themes/airbnb.css'

import NavBar from '@/views/NavBar'
import './common.scss'

/* eslint-disable no-new */
new Vue({
  el: '#navbar',
  data: {
    expanded: false
  },
  components: { NavBar }
})
