import axios from "../utils/axios";

// const PER_PAGE = 30;

export default {
  namespaced: true,
  state: {
    messages: [
      {
        id: 1,
        title: "title example",
        content: "shorted content",
        html: "html content",
        sender: "send user short name",
        writer: "write user short name",
        created_at: "2021/12/24 (金) 10:10",
        updated_at: "2021/12/24 (金) 10:10",// sort key
        is_bookmarked: false
      }
    ],
    query: {}
  },
  mutations: {
    addMessages (state, payload) {
      // payload: Array of Object (message)
      state.messages = state.messages.concat(payload);
    },
    clearMessage (state) {
      state.messages.length = 0;
    }
  },
  actions: {
    async firstLoadMessage ({dispatch}) {
      await dispatch('loadMessages', { page:1 })
    },
    async loadMessages (context, params) {
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