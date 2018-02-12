// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable import/first */
import Vue, { store } from './base'

import 'bootstrap-vue/dist/bootstrap-vue.css'

import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'flatpickr/dist/themes/airbnb.css'

import './common.scss'

import NavBar from '@/views/NavBar'

/* eslint-disable no-new */
new Vue({
  el: '#navbar',
  store,
  data: {
    expanded: false
  },
  components: { NavBar }
})
