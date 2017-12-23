// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import FontAwesomeIcon from '@fortawesome/vue-fontawesome'

import NavBar from './components/NavBar'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import 'vue-multiselect/dist/vue-multiselect.min.css'

import './main.css'

Vue.config.productionTip = false

Vue.use(BootstrapVue)

/* eslint-disable no-new */
new Vue({
  el: '#navbar',
  components: { NavBar, FontAwesomeIcon }
})
