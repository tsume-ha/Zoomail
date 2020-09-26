import axios from 'axios';

export default {
  namespaced: true,
  state: {
    messages: [],
    page: 1,
  },
  mutations: {
    addMessages (state, payload) {
      state.messages = state.messages.concat(payload);
      console.log(state.messages)
    },
    pageUpdate (state, payload) {
      state.page = payload;
      console.log(state.page)
    },
  },
  actions: {
    loadMessages (context) {
      if (context.state.messages.length > 0) {
        return;
      }
      axios.get('/read/_/json/', {
        params: {
          'page': context.state.page
        }
      })
        .then(res => {
          context.commit('addMessages', res.data.message_list);
          context.commit('pageUpdate', context.state.page + 1);
          return new Promise();
        })
    }
  }
}