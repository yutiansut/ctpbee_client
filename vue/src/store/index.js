import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    token: ''
  },
  mutations: {
    setToken: function(state, userToken) {
      state.token = userToken
    },
    clearToken: function(state) {
      state.token = null
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
