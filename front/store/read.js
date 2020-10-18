import axios from 'axios';

export default {
  namespaced: true,
  state: {
    messages: [],
    loadNum: 10,
  },
  mutations: {
    addMessages (state, payload) {
      state.messages = state.messages.concat(payload);
      console.log(state.messages)
    },
  },
  actions: {
    async loadMessages (context) {
      const page = Math.ceil(context.state.messages.length / context.state.loadNum) + 1;
      console.log('vuex _ access url: ', String(page));
      return await axios.get('/read/_/json/', {
        params: {
          'page': page
        }
      })
      .then(res => {
        context.commit('addMessages', res.data.message_list);
        return res.data;
      })          
    }
  }
}