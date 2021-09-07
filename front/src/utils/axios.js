import axios from 'axios'
import Cookies from 'js-cookie'

const instance = axios.create({
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  },
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN"
});


export default async function(kwargs) {
  return await instance(kwargs).then(res => {
    // cookieからメッセージを取り出す
    const allCookies = Cookies.get();
    const reg = /^message_\d\d_/
    const messageKeys = Object.keys(allCookies).filter(item => reg.test(item))
    let result = [];
    for (const key of messageKeys) {
      const level = key.replace(reg, "")
      result.push({
        level: level,
        message: allCookies[key]
      })
      Cookies.remove(key)
    }

    console.log(result)

    return res
  })
}