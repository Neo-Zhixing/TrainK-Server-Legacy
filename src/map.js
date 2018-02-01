import App from '@/map/App'
import Vue from 'vue'
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#map-container',
  template: '<App/>',
  components: { App }
})
