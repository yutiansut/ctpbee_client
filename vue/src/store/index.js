import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    width: ''
  },
  mutations: {
    setWidth(state, width) {
      state.width = width
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
