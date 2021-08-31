import Vue from 'vue'
import Vuex from 'vuex'

import read from './read'
import send from './send'
import members from './members'

Vue.use(Vuex)

export default new Vuex.Store({
    strict: true,
    modules: {
        read,
        send,
        members
    },

})