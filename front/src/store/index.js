import { createStore } from 'vuex'
import message from './message'
import user from './user'
import read from './read'
import send from './send'
import sound from './sound'
import mypage from './mypage'

export default createStore({
  strict: process.env.NODE_ENV !== 'production',
  state: {
    lastPath: null,
  },
  mutations: {
    updateLastPath(state, payload) {
      state.lastPath = payload;
    }
  },
  actions: {
  },
  modules: {
    message,
    user,
    read,
    send,
    sound,
    mypage
  }
})
