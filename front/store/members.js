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
    getUserInfo (context) {
      axios.get('/mypage/api/user/')
      .then(res => {
        console.log(res.data)
        context.commit('updateUserInfo', res.data)
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}