import axios from "../utils/axios";

export default {
  namespaced: true,
  state: {
    id: null,
    shortname: "",
    year: null,
    is_staff: false,
    data_fetched: null,
  },
  mutations: {
    set (state, payload) {
      // 一時的に
      const keys = ["id", "shortname", "year", "is_staff"];
      for (const key of keys) {
        state[key] = payload[key];
      }
      state.data_fetched = new Date();
    }
  },
  actions: {
    getUserInfo(context) {
      axios.get("/api/mypage/user/").then(res => {
        context.commit("set", res.data);
      });
    }
  }
};
