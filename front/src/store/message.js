// import Vue from 'vue'
import Cookies from 'js-cookie'

export default {
  namespaced: true,
  state: {
    messages: {}
  },
  mutations: {
    storeMessageFromCokie(state) {
      // cookieからメッセージを取り出す
      const allCookies = Cookies.get();
      const reg = /^message_\d\d\d\d\d\d\d\d\d\d_\d\d_/;
      const messageKeys = Object.keys(allCookies).filter(item => reg.test(item));
      for (const key of messageKeys) {
        const level = key.replace(reg, "");
        state.messages = {...state.messages, [key]: {
          level: level,
          message: allCookies[key],
          displayed: false,
          completed: false,
        }}
        Cookies.remove(key)
      }
    },
    displayed(state, payload) {
      if(Object.hasOwnProperty.call(state.messages, payload)){
        state.messages[payload] = {...state.messages[payload], displayed: true}
      }
    },
    completed(state, payload) {
      if(Object.hasOwnProperty.call(state.messages, payload)){
        state.messages[payload] = {...state.messages[payload], completed: true}
      }
    }
  }
}