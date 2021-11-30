import axios from "../utils/axios";
import moment from "../utils/moment";

export default {
  namespaced: true,
  state: {
    lives: [],
    updated: null
  },
  mutations: {
    set (state, payload) {
      state.lives.length = 0;
      state.lives.push(...payload);
      state.updated = moment();
    }
  },
  actions: {
    getSoundsFromAPI(context) {
      if (context.state.lives.length == 0 || 
          context.state.updated.isBefore( moment().subtract(1, "hours") )
         ) {
          axios.get("/api/sound/").then(res => {
            context.commit("set", res.data.lives);
          });
      }
    },
    loadOneSoundContent(context) {
      axios.get("/api/sound/").then(res => {
        context.commit("set", res.data.lives);
      });
    }
  }
};
