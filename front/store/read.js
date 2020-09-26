import axios from 'axios';

export default {
  namespaced: true,
  state: {
    messages: [],
  },
  mutations: {
    addMessages (state, payload) {
      console.log(payload)
      state.messages = state.messages.concat(payload);
    },
  },
  actions: {
    loadMessages (context) {
      if (context.state.messages.length > 0) {
        return;
      }
      axios.get('/read/_/json/')
        .then(res => {
          context.commit('addMessages', res.data.message_list);
        })
    }
  }
}