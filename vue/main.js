// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import FontAwesomeIcon from '@fortawesome/vue-fontawesome'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import './main.css'


Vue.config.productionTip = false

Vue.use(BootstrapVue)


import NavBar from './components/NavBar'


/* eslint-disable no-new */
new Vue({
  el: '#navbar',
  components: { NavBar, FontAwesomeIcon }
})
