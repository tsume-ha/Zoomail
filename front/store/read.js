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
    clearMessages (state) {
      state.messages.length = 0;
    }
  },
  actions: {
    async loadMessages (context, data) {
      const page = Math.ceil(context.state.messages.length / context.state.loadNum) + 1;
      let params = {};
      if (data) {
        params = data;
      }
      params['page'] = page;
      console.log('vuex _ access url: ', String(page));
      return await axios.get('/read/api/json/', {
        params: params
      })
      .then(res => {
        context.commit('addMessages', res.data.message_list);
        return res.data;
      })          
    }
  }
}