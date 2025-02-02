import axios from "../utils/axios";
// import moment from "../utils/moment";


export default {
  namespaced: true,
  state: {
    loading: false,
    userInfo: {}
  },
  mutations: {
    setLoading(state, bool) {
      state.loading = bool;
    },
    setUserInfo(state, payload) {
      state.userInfo = { ...payload };
    }
  },
  getters: {
    hasUserInfo(state) {
      return Object.keys(state.userInfo).length > 0;
    }
  },
  actions: {
    post(context, payload) {
      context.commit("setLoading", true);
      const { path, formData } = payload;
      const headers = { "content-type": "multipart/form-data" };
      axios.post(path, formData, { headers }).then(res => {
        context.commit("setUserInfo", res.data.userInfo);
      }).catch(error => {
        if (error.response === undefined) {
          // 通信エラー
        } else {
          // 400 など
        }
      }).finally(() => {
        context.commit("setLoading", false);
      });
    },
    getUserInfo(context) {
      context.commit("setLoading", true);
      axios.get("/api/mypage/user/").then(res => {
        context.commit("setUserInfo", res.data.userInfo);
      }).finally(() => {
        context.commit("setLoading", false);
      });
    }
  }
};
