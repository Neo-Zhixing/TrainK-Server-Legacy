import Vue from 'vue'
import Router from 'vue-router'
import DelayChartView from '../components/DelayChartView'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: '/query',
  routes: [
    {
      path: '/train',
      name: 'DelayChart',
      component: DelayChartView
    }
  ]
})
