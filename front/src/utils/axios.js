import axios from 'axios'
import store from '../store'

const instance = axios.create({
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  },
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN"
});

instance.interceptors.response.use((response) => {
  store.commit('message/storeMessageFromCokie');
  return response;
});

export default instance;
