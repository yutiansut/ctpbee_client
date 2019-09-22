import Vue from 'vue'
import 'normalize.css/normalize.css'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/styles/index.scss'
import App from './App'
import store from './store'
import router from './router'
import '@/icons' // icon
import '@/assets/css/font/iconfont.css'
//全局使用axios、qs
import axios from 'axios'
import qs from 'qs'
Vue.prototype.$axios = axios
const URL = 'http://10.40.25.15:5000/'
axios.defaults.baseURL = URL
//请求拦截器
axios.interceptors.request.use(config => {
  config.headers.Authorization = 'JWT ' + sessionStorage.getItem('token')
  if (config.method === 'post'||config.method === 'put') {
    config.data = qs.stringify(config.data)
  }
  return config
})

//使用ElementUI
Vue.use(ElementUI, {})
//引入socket
import VueSocketIO from 'vue-socket.io'
Vue.use(new VueSocketIO({
  connection: URL
}))
//使用animate.css实现动画
import animated from 'animate.css'
Vue.use(animated)

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

import tips from '@/assets/globalMethod/tips'
// 提示框
Vue.use(tips)
// 自定义全局指令---实现拖拽和伸缩效果
Vue.directive('drag', {
  bind: function (el) {
    let div = el // 获取当前元素
    //拖拽图标
    div.onmousemove = function (el) {
      var disX = el.clientX - div.offsetLeft;
      var disY = el.clientY - div.offsetTop;
      if ((disX <= 10 && disY <= 10) || (disX >= (div.offsetWidth - 10) && disY >= (div.offsetHeight - 10))) {
        div.style.cursor = "nwse-resize"
      } else if ((disX <= 10 && disY >= (div.offsetHeight - 10)) || (disY <= 10 && disX >= (div.offsetWidth - 10))) {
        div.style.cursor = "nesw-resize"
      } else if (disX <= 10 || disX >= (div.offsetWidth - 10)) {
        div.style.cursor = "ew-resize"
      } else if (disY <= 10 || disY >= (div.offsetHeight - 10)) {
        div.style.cursor = "ns-resize"
      } else {
        div.style.cursor = ""
      }
    }
    div.onmousedown = (e) => {
      // 算出鼠标相对元素的位置
      let disX = e.clientX - div.offsetLeft
      let disY = e.clientY - div.offsetTop
      //盒子高宽
      let divW = div.offsetWidth
      let divH = div.offsetHeight
      //可视区域宽高
      let clientH = document.body.clientHeight
      let clientW = document.body.clientWidth
      //距离左边最大距离
      let divL = clientW - divW
      //距离顶部最大距离
      let divT = clientH - divH
      //拉伸时记录鼠标的当前位置
      let oldX = e.clientX;
      let oldY = e.clientY;

      document.onmousemove = (e) => {
        if (disX > 10 && disY > 10 && disY < (div.offsetHeight - 10) && disX < (div.offsetWidth - 10)) {
          div.style.cursor = "grabbing"
          // 用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
          let left = e.clientX - disX <= 0 ? 0 : e.clientX - disX >= divL ? divL : e.clientX - disX
          let top = e.clientY - disY <= 0 ? 0 : e.clientY - disY >= divT ? divT : e.clientY - disY
          // 移动当前元素
          div.style.left = left + 'px';
          div.style.top = top + 'px';
        } else {
          if (disX <= 10) { //当鼠标向左拖动时
            // 元素当前的left值（此时ev.clientX - oldX为负值）
            div.style.left = div.offsetLeft + (e.clientX - oldX) + 'px';
            // 元素当前的宽度
            div.style.width = div.offsetWidth - (e.clientX - oldX) + 'px';
          } else if (disX >= (div.offsetWidth - 10)) { //当鼠标向右拖动时
            div.style.width = div.offsetWidth + (e.clientX - oldX) + 'px';
            //由于向右拉伸，盒子增大，鼠标的相对位置也发生改变，故此时需重新获取该值
            disX = e.clientX - div.offsetLeft;
          }
          if (disY <= 10) { //当鼠标向上拖动时（此时ev.clientX - oldX为负值）
            div.style.top = div.offsetTop + (e.clientY - oldY) + 'px';
            div.style.height = div.offsetHeight - (e.clientY - oldY) + 'px';
          } else if (disY >= (div.offsetHeight - 10)) { //当鼠标向下拖动时
            div.style.height = div.offsetHeight + (e.clientY - oldY) + 'px';
            //由于向下拉伸，盒子增大，鼠标的相对位置也发生改变，故此时需重新获取该值
            disY = e.clientY - div.offsetTop;
          }
          //拉伸完毕之后，由于盒子经过了缩放，边界位置改变，故此时重新获取鼠标位置
          oldX = e.clientX;
          oldY = e.clientY;
        }
      }
      document.onmouseup = (e) => {
        document.onmousemove = null;
        document.onmouseup = null;
      }
    }
  }
})
// 创建Vue实例
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
