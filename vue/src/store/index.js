import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    token: '',
    flag: true,
    clearTimer: true
  },
  mutations: {
    closeFlag: function(state, close) {
      state.flag = close
    },
    clear: function(state, close) {
      state.clearTimer = close
    }
  },
  modules: {
    app,
    settings,
    user
  },
  getters
})

export default store
