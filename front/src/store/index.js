import { createStore } from 'vuex'
import message from './message'

export default createStore({
  strict: process.env.NODE_ENV !== 'production',
  state: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    message,
  }
})
