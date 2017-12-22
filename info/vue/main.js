// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import DelayChartCard from './components/DelayChartCard'
import InfoHomeTab from './components/InfoHomeTab'

import FontAwesomeIcon from '@fortawesome/vue-fontawesome'

import fontawesome from '@fortawesome/fontawesome'
import { faLongArrowAltRight } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faLongArrowAltRight)

Vue.config.productionTip = false

Vue.use(BootstrapVue)

/* eslint-disable no-new */
new Vue({
  el: '#entrance',
  components: { DelayChartCard, InfoHomeTab, FontAwesomeIcon }
})
