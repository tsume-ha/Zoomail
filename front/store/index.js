import Vue from 'vue'
import Vuex from 'vuex'

import read from './read'

Vue.use(Vuex)

export default new Vuex.Store({
    strict: true,
    namespaced: true,
    modules: {
        read,
    },

})