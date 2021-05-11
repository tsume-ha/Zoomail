import axios from 'axios';

export default {
  namespaced: true,
  state: {
    user: {}
  },
  mutations: {
    updateUserInfo (state, payload) {
      state.user = payload;
    }
  },
  actions: {
    async getUserInfo (context) {
      return await axios.get('/api/mypage/user/')
      .then(res => {
        context.commit('updateUserInfo', res.data)
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}