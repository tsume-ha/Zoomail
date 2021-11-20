import { createStore } from 'vuex'
import message from './message'
import user from './user'
import read from './read'
import send from './send'
import sound from './sound'

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
    user,
    read,
    send,
    sound
  }
})
