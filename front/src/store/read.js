import axios from "../utils/axios";

export default {
  namespaced: true,
  state: {
    messages: [
      // {
      //   id: 0,
      //   title: "title example",
      //   content: "shorted content",
      //   html: "html content",
      //   sender: "send user short name",
      //   writer: "write user short name",
      //   created_at: "2021/12/24 (金) 10:10",
      //   updated_at: "2021/12/24 (金) 10:10",// sort key
      //   is_bookmarked: false
      // }
    ],
    params: {},
    nowLoading: false,
  },
  mutations: {
    setMessages (state, messages) {
      state.messages.length = 0;
      state.messages = messages;
    },
    startAPILoading (state) {
      state.nowLoading = true;
      console.log('startAPILoading');
    },
    finishAPILoading (state) {
      state.nowLoading = false;
      console.log('finishAPILoading');
    },
    updateBookmarked (state, payload) {
      const target = state.messages.find(item => item.id === payload.id);
      if (target) {
        // state.messages[]が空でtargetがundefinedになってる場合を弾く
        target.is_bookmarked = payload.bool;
      }
    },
    updateParams (state, payload) {
      state.params = payload;
    }
  },
  actions: {
    getMessagesFromAPI (context, params) {
      // APIを叩く
      context.commit('startAPILoading');
      axios.get('/api/board/json/', {params}).then(res => {
        // messages を更新;
        context.commit('setMessages', res.data.message_list);
        context.commit('updateParams', params);
      })
      .catch(e => {
        console.log("name", e.name);
        console.log("message", e.message);
        console.log("response", e.response);
        console.log("response.status", e.response.status);
      }).finally(() => {
        context.commit('finishAPILoading');
      });
    },
    async loadOneMessage (context, id) {
      context.commit('startAPILoading');
      const res = await axios.get('/api/board/content/' + String(id) + '/')
      .catch(e => {
        console.log("name", e.name);
        console.log("message", e.message);
        console.log("response", e.response);
        console.log("response.status", e.response.status);
      });
      context.commit('finishAPILoading');
      context.commit('setMessages', [res.data.message]);
      return res.data.message;
    },
    toggleBookmark (context, id) {
      const message = context.state.messages.find(item => item.id === id);
      context.commit('updateBookmarked', {
        'id': id,
        'bool': !message.is_bookmarked
      });
      axios.post('/api/board/bookmark/' + String(id) +'/', {
        'data': 'data'
      }).then(res => {
        context.commit('updateBookmarked', {
          'id': id,
          'bool': (res.data['updated-to'] === 'true')
        });
      });
    }
  }
};