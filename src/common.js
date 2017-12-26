// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable import/first */
import Vue from 'vue'
Vue.config.productionTip = false

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)
import {
  faTrain,
  faBars,
  faUserCircle,
  faSignOutAlt,
  faSignInAlt,
  faCloud,

  faTicketAlt,
  faInfoCircle,
  faBriefcase,
  faMap,
  faComments
} from '@fortawesome/fontawesome-free-solid'
import fontawesome from '@fortawesome/fontawesome'
fontawesome.library.add(faTrain, faBars, faUserCircle, faSignInAlt, faSignOutAlt, faCloud)
fontawesome.library.add(faTicketAlt, faInfoCircle, faBriefcase, faMap, faComments)

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import 'vue-multiselect/dist/vue-multiselect.min.css'

import '@/common.css'

/* eslint-disable no-new */
new Vue({
  el: '#navbar',
  data: {
    expanded: false
  },
  components: { }
})
