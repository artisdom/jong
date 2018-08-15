import Vue from 'vue'
import Router from 'vue-router'
import RssList from '@/components/RssList'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', name: 'RssList', component: RssList }
  ]
})
