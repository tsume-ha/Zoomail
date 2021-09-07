import axios from 'axios'
import store from '../store'

const instance = axios.create({
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  },
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN"
});


export default async function(kwargs) {
  return await instance(kwargs).then(res => {
    store.commit('message/storeMessageFromCokie');
    return res
  })
}