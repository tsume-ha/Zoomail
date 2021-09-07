import Cookies from 'js-cookie'

export default {
  namespaced: true,
  state: {
    messages: []
  },
  mutations: {
    storeMessageFromCokie(state) {
      // cookieからメッセージを取り出す
      const allCookies = Cookies.get();
      const reg = /^message_\d\d_/;
      const messageKeys = Object.keys(allCookies).filter(item => reg.test(item));
      for (const key of messageKeys) {
        const level = key.replace(reg, "");
        state.messages = [...state.messages, {
          level: level,
          message: allCookies[key],
          complete: false
        }]
        Cookies.remove(key)
      }
    }
  }
}