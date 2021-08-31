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
      // console.log(state.messages)
    },
    clearMessages (state) {
      state.messages.length = 0;
    },
    updateBookmarked (state, payload) {
      // payload: {id: <id>, bool: <Boolean>}
      const target = state.messages.find(content => content.id == String(payload.id))
      if (target) {
        // contentに直接したときは
        // state.messages[]が空でundefinedになってる
        target.is_bookmarked = payload.bool;
      }
    },
  },
  actions: {
    async loadMessages (context, data) {
      const page = Math.ceil(context.state.messages.length / context.state.loadNum) + 1;
      let params = {};
      if (data) {
        params = data;
      }

      params['page'] = page;
      
      return await axios.get('/api/board/json/', {
        params: params
      })
      .then(res => {
        context.commit('addMessages', res.data.message_list);
        return res.data;
      })          
    }
  }
}