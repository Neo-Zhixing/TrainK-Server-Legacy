// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable import/first */
import Vue from 'vue'
Vue.config.productionTip = false

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)
import fontawesome from '@fortawesome/fontawesome'
import { faLongArrowAltRight, faUniversity } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faLongArrowAltRight, faUniversity)

import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

import DelayChartCard from '@/components/info/DelayChartCard'
import HomeTab from '@/components/info/HomeTab'

/* eslint-disable no-new */
new Vue({
  el: '#entrance',
  components: { DelayChartCard, HomeTab }
})
