// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'

import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

let Cookies = require('js-cookie')

let csrftoken = Cookies.get('csrftoken')

axios.defaults.headers.common['cookiename'] = 'csrftoken'
axios.defaults.headers.common['X-CSRFToken'] = csrftoken
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
axios.defaults.headers.common['access-control-allow-origin'] = '*'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
