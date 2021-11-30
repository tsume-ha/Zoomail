// import Vue from 'vue'
import Cookies from "js-cookie";

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
        }};
        Cookies.remove(key);
      }
    },
    displayed(state, payload) {
      // payload: key String
      if(Object.hasOwnProperty.call(state.messages, payload)){
        state.messages[payload] = {...state.messages[payload], displayed: true};
      }
    },
    completed(state, payload) {
      // payload: key String
      if(Object.hasOwnProperty.call(state.messages, payload)){
        state.messages[payload] = {...state.messages[payload], completed: true};
      }
    },
    addMessage(state, payload) {
      // payload: object, {level: String, message: String, appname: String}
      const key = `local_${payload.appname}${String(Object.keys(state.messages).length + 1)}`;
      state.messages = {...state.messages, [key]: {
        level: payload.level,
        message: payload.message,
        displayed: false,
        completed: false,
      }};
    }
  }
};