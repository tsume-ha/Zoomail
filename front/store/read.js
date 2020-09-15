import axios from 'axios';

export default {
  namespaced: true,
  state: {
    test: 'hogefuga',
    messages: [

    ],
  },
  mutations: {
    addMessages (state, payload) {
      state.messages += payload;
    },
  },
  actions: {
    loadMessages (context) {
      axios.get('/read/_/json/')
        .then(res => {
          console.log(res);
          context.commit('addMessages', res.data.message_list);
        })
    }
  }
}