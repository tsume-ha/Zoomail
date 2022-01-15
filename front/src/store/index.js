import { createStore } from "vuex";
import message from "./message";
import user from "./user";
import read from "./read";
import send from "./send";
import sound from "./sound";
import mypage from "./mypage";

export default createStore({
  strict: process.env.NODE_ENV !== "production",
  state: {
    lastPath: null,
    menuStatus: "menuClosed"
  },
  mutations: {
    updateLastPath(state, payload) {
      state.lastPath = payload;
    },
    setMenuStatus(state, payload) {
      if (["menuClosed", "menuOpened", "detail"].indexOf(payload) !== -1) {
        state.menuStatus = payload;
      } else {
        throw new Error("invlid menu status");
      }
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
});
