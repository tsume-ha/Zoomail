import axios from "../utils/axios";
import db from "../utils/db";

const PER_PAGE = 30;

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
    query: {},
    updated: null,// Date
    nowLoading: false,
  },
  mutations: {
    addMessages (state, messages) {
      // messages: Array of Object (message)
      // new ... [a, b, c] + [c, d, e, f] => [a, b, c, d, e, f] ... old 
      // のような結合をしたい
      messages.reverse();
      // なるべく古い順から追加していく。
      for (const message of messages) {
        if (!state.messages.some(m => m.id === message.id)) {
          state.messages.unshift(message);
        }
      }
    },
    clearMessage (state) {
      state.messages.length = 0;
    },
    startAPILoading (state) {
      state.nowLoading = true;
      console.log('startAPILoading')
    },
    finishAPILoading (state) {
      state.nowLoading = false;
      console.log('finishAPILoading')
    },
    updateBookmarked (state, payload) {
      const target = state.messages.find(item => item.id === payload.id)
      if (target) {
        // state.messages[]が空でtargetがundefinedになってる場合を弾く
        target.is_bookmarked = payload.bool;
      }
    }
  },
  actions: {
    async firstLoadMessage (context) {
      // 1度だけ必ずAPIから取得し、非同期でDBとVuexを更新する

      // localDBから取得を試みる
      db.messages.orderBy("updated_at").reverse().limit(PER_PAGE).toArray().then(cached => {
        context.commit('addMessages', cached)
      }).catch(error => {
        // localDB失敗
        console.log(error)
      })

      // APIを叩いてVuexを更新。localDBにも保存。
      context.dispatch('getMessagesFromAPI', { page:1 }).then(messages => {
        context.commit('addMessages', messages);
        return messages;
      }).then(messages => {
        context.dispatch('addLocalDB', messages).catch(() => {
          console.log('Local DB add was fail.')
        })
      })
    },
    async getMessagesFromAPI (context, params) {
      // APIを叩く
      context.commit('startAPILoading');
      const res = await axios.get('/api/board/json/', {params})
      .catch(e => {
        console.log("name", e.name)
        console.log("message", e.message)
        console.log("response", e.response)
        console.log("response.status", e.response.status)
      })
      context.commit('finishAPILoading')

      // page数などの更新
      
      // messages を返す
      console.log('messages from API', res.data.message_list)
      return res.data.message_list;
    },
    async addLocalDB (context, messages) {
      // localDBに保存する。
      // 保存前の最新のメーリスまで更新できなかったときは、
      // 間に未取得のメーリスがあるとしてそれまでのデータを消しておく。
      // [a, b, c] + [c, d, e] => [a, b, c, d, e, f]
      // [a, b, c] + [g, h ,i] => [a, b, c]
      const lastMessageBeforeAdd = await db.messages.orderBy("updated_at").reverse().first();
      const lastKey = await db.messages.bulkPut(messages);
      const lastData = await db.messages.get(lastKey);
      if (new Date(lastData.updated_at).getTime() > new Date(lastMessageBeforeAdd.updated_at).getTime()) {
        await db.messages.filter(item => {
          new Date(lastData.updated_at).getTime() > new Date(item.updated_at).getTime()
        }).delete();
      }
    },
    async loadOneMessage (context, id) {
      const res = await axios.get('/api/board/content/' + String(id) + '/');
      context.commit('addMessages', [res.data.message]);
      return res.data.message;
    },
    toggleBookmark (context, id) {
      const message = context.state.messages.find(item => item.id === id);
      context.commit('updateBookmarked', {
        'id': id,
        'bool': !message.is_bookmarked
      })
      axios.post('/api/board/bookmark/' + String(id) +'/', {
        'data': 'data'
      }).then(res => {
        context.commit('updateBookmarked', {
          'id': id,
          'bool': (res.data['updated-to'] === 'true')
        })
        return res.data['updated-to'] === 'true';
      }).then(bool => {
        return db.messages.get(id).then(message => {
          message.is_bookmarked = bool;
          return db.messages.put(message);
        })
      })
    }
  }
}