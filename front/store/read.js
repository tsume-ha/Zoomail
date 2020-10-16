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
    async loadMessages (context) {
      console.log('vuex _ access url: ', String(context.state.page));
      context.commit('pageUpdate', context.state.page + 1);
      // 先にpage数を追加しておく
      // responseが帰ってくる前にpage数は変えておきたい
      await axios.get('/read/_/json/', {
        params: {
          'page': context.state.page - 1
          // ここで引いておく
        }
      })
      .then(res => {
        context.commit('addMessages', res.data.message_list);
        console.log('vuex _ action done')
      });
          
    }
  }
}