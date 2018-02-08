/* eslint-disable import/first */
import Vue from 'vue'
Vue.config.productionTip = false

import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import VeeValidate from 'vee-validate'
Vue.use(VeeValidate)

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)

export default Vue
