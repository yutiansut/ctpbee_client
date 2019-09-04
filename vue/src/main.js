import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import locale from 'element-ui/lib/locale/lang/en'

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import '@/icons' // icon
import '@/permission' // permission control

import axios from 'axios'
import qs from 'qs'
Vue.prototype.$axios = axios
// axios.interceptors.request.use(
//   config => {
//     const token = sessionStorage.getItem('token')
//     if (token) {
//       config.headers.common['MToken'] = token
//     }
//     if (store.state.uid) {
//       config.headers.common['UID'] = store.state.uid
//     }
//     return config
//   },
//   err => {
//     return Promise.reject(err)
//   })
Vue.prototype.$qs = qs

const URL = 'http://10.40.25.15:5000'
// const URL = 'http://10.200.42.176:5000'
Vue.prototype.URL = URL

Vue.use(ElementUI, {})

import VueSocketIO from 'vue-socket.io'
// import socketIO from 'socket.io-client'
Vue.use(new VueSocketIO({
  connection: URL
}))

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online! ! !
 */
import {
  mockXHR
} from '../mock'
if (process.env.NODE_ENV === 'production') {
  mockXHR()
}

Vue.config.productionTip = false

Vue.prototype.tip = (type, msg, that) => {
  that.$message({
    showClose: true,
    message: msg,
    type: type
  })
}

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})

router.beforeEach(function(to, from, next) {
  const token = sessionStorage.getItem('token')
  if (token) {
    next()
  } else {
    if (to.path === '/login') {
      next()
    } else {
      next({
        path: '/login'
      })
    }
  }
})