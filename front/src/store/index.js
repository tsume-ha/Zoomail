import { createStore } from 'vuex'
import message from './message'
import send from './send'

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
    send
  }
})
