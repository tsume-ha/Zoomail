(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[64],{7355:function(e,s,t){var a={"./ja":9183,"./ja.js":9183,"moment/locale/ja":9183,"moment/locale/ja.js":9183};function o(e){var s=n(e);return t(s)}function n(e){if(!t.o(a,e)){var s=new Error("Cannot find module '"+e+"'");throw s.code="MODULE_NOT_FOUND",s}return a[e]}o.keys=function(){return Object.keys(a)},o.resolve=n,e.exports=o,o.id=7355},2837:function(e,s,t){"use strict";t.d(s,{Z:function(){return h}});var a=t(3907),o=t(114),n=t(8042),r={namespaced:!0,state:{id:null,shortname:"",year:null,is_staff:!1,data_fetched:null},mutations:{set(e,s){const t=["id","shortname","year","is_staff"];for(const a of t)e[a]=s[a];e.data_fetched=new Date}},actions:{getUserInfo(e){n.Z.get("/api/mypage/user/").then((s=>{console.log(s.data),e.commit("set",s.data)}))}}},i={namespaced:!0,state:{messages:[],params:{},nowLoading:!1,totalPages:0},mutations:{setMessages(e,s){e.messages.length=0,e.messages=s},startAPILoading(e){e.nowLoading=!0,console.log("startAPILoading")},finishAPILoading(e){e.nowLoading=!1,console.log("finishAPILoading")},updateBookmarked(e,s){const t=e.messages.find((e=>e.id===s.id));t&&(t.is_bookmarked=s.bool)},updateParams(e,s){e.params=s},setTotalPages(e,s){e.totalPages=Number(s)}},actions:{getMessagesFromAPI(e,s){e.commit("startAPILoading"),n.Z.get("/api/board/json/",{params:s}).then((t=>{e.commit("setMessages",t.data.messages),e.commit("updateParams",s),e.commit("setTotalPages",t.data.paginator.total)})).catch((e=>{console.log("name",e.name),console.log("message",e.message),console.log("response",e.response),console.log("response.status",e.response.status)})).finally((()=>{e.commit("finishAPILoading")}))},async loadOneMessage(e,s){e.commit("startAPILoading");const t=await n.Z.get(`/api/board/content/${String(s)}/`).catch((e=>{console.log("name",e.name),console.log("message",e.message),console.log("response",e.response),console.log("response.status",e.response.status)}));return e.commit("finishAPILoading"),e.commit("setMessages",[t.data.message]),t.data.message},toggleBookmark(e,s){const t=e.state.messages.find((e=>e.id===s));e.commit("updateBookmarked",{id:s,bool:!t.is_bookmarked}),n.Z.post(`/api/board/bookmark/${String(s)}/`,{data:"data"}).then((t=>{e.commit("updateBookmarked",{id:s,bool:"true"===t.data["updated-to"]})}))}}};t(7658);function l(e){const s=[];return e.length<1&&s.push("タイトルを入力してください"),e.length>200&&s.push("タイトルが長すぎます"),s}function c(e){const s=[];e.length<1&&s.push("本文を入力してください");const t=/[\w\-._]+@[\w\-._]+\.[A-Za-z]+/,a=/https?:\/\/[\w!?/+\-_~;.,*&@#$%()'[\]]+/;if(e.search(t)>0){const a=e.search(t);"\n"!==e[a-1]&&" "!==e[a-1]&&s.push("メールアドレスの前後には改行または半角スペースを入れてください")}if(e.search(a)>0){const t=e.search(a);"\n"!==e[t-1]&&" "!==e[t-1]&&s.push("URLの前後には半角スペースを入れてください")}return s}function m(e){const s=[];return e||s.push("差出人を指定してください"),s}function d(e){const s=[];return null===e?["宛先を指定してください"]:(e&&0!==e.length||s.push("宛先を指定してください"),s)}function u(e){const s=[];if(0===e.length)return[];let t=0;for(const a of e)a.size||s.push("ファイルが無効です"),a.size<0&&s.push("ファイルが無効です(zero file size)"),a.size>1e7&&s.push(`ファイルサイズが上限(10MB)を超えています：${a.name}`),t+=a.size;return t>20971520&&s.push("合計のファイルサイズが上限(20MB)を超えています"),s}var g={namespaced:!0,state:{title:{value:"",is_dirty:!1,error_messages:[]},content:{value:"",is_dirty:!1,error_messages:[]},tos:{value:[],is_dirty:!1,error_messages:[]},writer:{value:null,is_dirty:!1,error_messages:[]},attachments:{value:[],is_dirty:!1,error_messages:[]},send_at:{value:null,is_dirty:!1,error_messages:[]}},mutations:{setTitle(e,s){e.title.value=s,e.title.error_messages=l(e.title.value),e.title.is_dirty=!0},setContent(e,s){e.content.value=s,e.content.error_messages=c(e.content.value),e.content.is_dirty=!0},setTos(e,s){e.tos.value=s,e.tos.error_messages=d(e.tos.value),e.tos.is_dirty=!0},setWriter(e,s){e.writer.value=s,e.writer.error_messages=m(e.writer.value),e.writer.is_dirty=!0},setAttachments(e,s){e.attachments.value=s,e.attachments.error_messages=u(e.attachments.value),e.attachments.is_dirty=!0},validateAll(e){e.title.error_messages=l(e.title.value),e.content.error_messages=c(e.content.value),e.writer.error_messages=m(e.writer.value),e.attachments.error_messages=u(e.attachments.value),e.title.is_dirty=!0,e.content.is_dirty=!0,e.writer.is_dirty=!0,e.attachments.is_dirty=!0},reset(e){e.title={value:"",is_dirty:!1,error_messages:[]},e.content={value:"",is_dirty:!1,error_messages:[]},e.tos={value:[],is_dirty:!1,error_messages:[]},e.writer={value:null,is_dirty:!1,error_messages:[]},e.attachments={value:[],is_dirty:!1,error_messages:[]},e.send_at={value:null,is_dirty:!1,error_messages:[]}}},getters:{isValid(e){return!e.title.error_messages.length&&!e.content.error_messages.length&&!e.tos.error_messages.length&&!e.writer.error_messages.length&&!e.attachments.error_messages.length&&!e.send_at.error_messages.length},isValidAndDirty(e,s){return s.isValid&&e.title.is_dirty&&e.content.is_dirty}},actions:{send(e){if(e.commit("validateAll"),!e.getters.isValid)return e.commit("message/addMessage",{level:"error",message:"不正なフィールドがあり、送信できませんでした。",appname:"mail/send"},{root:!0}),Promise.reject(new Error("form validation error"));const s=new FormData;return s.append("title",e.state.title.value),s.append("content",e.state.content.value),e.state.tos.value.forEach((e=>{s.append("to",e.year)})),s.append("writer",e.state.writer.value.id),e.state.attachments.value.forEach((e=>{s.append("attachments",e)})),n.Z.post("/api/board/send/send/",s,{onUploadProgress:e=>console.log(e)})}}},p=t(5492),f={namespaced:!0,state:{lives:[],updated:null},mutations:{set(e,s){e.lives.length=0,e.lives.push(...s),e.updated=(0,p.Z)()}},actions:{getSoundsFromAPI(e){(0==e.state.lives.length||e.state.updated.isBefore((0,p.Z)().subtract(1,"hours")))&&n.Z.get("/api/sound/").then((s=>{e.commit("set",s.data.lives)}))},loadOneSoundContent(e){n.Z.get("/api/sound/").then((s=>{e.commit("set",s.data.lives)}))}}},v={namespaced:!0,state:{loading:!1,userInfo:{}},mutations:{setLoading(e,s){e.loading=s},setUserInfo(e,s){e.userInfo={...s}}},getters:{hasUserInfo(e){return Object.keys(e.userInfo).length>0}},actions:{post(e,s){e.commit("setLoading",!0);const{path:t,formData:a}=s,o={"content-type":"multipart/form-data"};n.Z.post(t,a,{headers:o}).then((s=>{e.commit("setUserInfo",s.data.userInfo)})).catch((e=>{e.response})).finally((()=>{e.commit("setLoading",!1)}))},getUserInfo(e){e.commit("setLoading",!0),n.Z.get("/api/mypage/user/").then((s=>{e.commit("setUserInfo",s.data.userInfo)})).finally((()=>{e.commit("setLoading",!1)}))}}},h=(0,a.MT)({strict:!1,state:{lastPath:null,menuStatus:"menuClosed"},mutations:{updateLastPath(e,s){e.lastPath=s},setMenuStatus(e,s){if(-1===["menuClosed","menuOpened","detail"].indexOf(s))throw new Error("invlid menu status");e.menuStatus=s}},actions:{},modules:{message:o.Z,user:r,read:i,send:g,sound:f,mypage:v}})},114:function(e,s,t){"use strict";var a=t(1955);s["Z"]={namespaced:!0,state:{messages:{}},mutations:{storeMessageFromCokie(e){const s=a.Z.get(),t=/^message_\d\d\d\d\d\d\d\d\d\d_\d\d_/,o=Object.keys(s).filter((e=>t.test(e)));for(const n of o){const o=n.replace(t,"");e.messages={...e.messages,[n]:{level:o,message:s[n],displayed:!1,completed:!1}},a.Z.remove(n)}},displayed(e,s){Object.hasOwnProperty.call(e.messages,s)&&(e.messages[s]={...e.messages[s],displayed:!0})},completed(e,s){Object.hasOwnProperty.call(e.messages,s)&&(e.messages[s]={...e.messages[s],completed:!0})},addMessage(e,s){const t=`local_${s.appname}${String(Object.keys(e.messages).length+1)}`;e.messages={...e.messages,[t]:{level:s.level,message:s.message,displayed:!1,completed:!1}}}}}},8042:function(e,s,t){"use strict";var a=t(9423),o=t(2837);const n=a.Z.create({headers:{"X-Requested-With":"XMLHttpRequest"},xsrfCookieName:"csrftoken",xsrfHeaderName:"X-CSRFTOKEN"});n.interceptors.response.use((e=>(o.Z.commit("message/storeMessageFromCokie"),e)),(e=>(o.Z.commit("message/storeMessageFromCokie"),Promise.reject(e)))),s["Z"]=501!=t.j?n:null},5492:function(e,s,t){"use strict";var a=t(381),o=t.n(a);t(9183);o()().format(),o()().locale("ja"),s["Z"]=501!=t.j?o():null},1542:function(e,s,t){"use strict";t.d(s,{Z:function(){return g}});var a=t(6252);const o=e=>((0,a.dD)("data-v-41315f7f"),e=e(),(0,a.Cn)(),e),n={class:"container"},r=o((()=>(0,a._)("span",null," © 2019-2022 京大アンプラグド ",-1))),i={href:"https://twitter.com/ku_unplugged_hp"},l={href:"https://github.com/tsume-ha/Zoomail"};function c(e,s){const t=(0,a.up)("Icon");return(0,a.wg)(),(0,a.iD)("footer",n,[r,(0,a._)("a",i,[(0,a.Wm)(t,{icon:["fab","twitter"]}),(0,a.Uk)(" Twitter ")]),(0,a._)("a",l,[(0,a.Wm)(t,{icon:["fab","github"]}),(0,a.Uk)(" GitHub ")])])}var m=t(3744);const d={},u=(0,m.Z)(d,[["render",c],["__scopeId","data-v-41315f7f"]]);var g=u},8337:function(e,s,t){"use strict";t.d(s,{Z:function(){return p}});var a=t(6252);const o={class:"container"};function n(e,s,t,n,r,i){const l=(0,a.up)("Icon"),c=(0,a.up)("router-link"),m=(0,a.up)("NavSW");return(0,a.wg)(),(0,a.iD)("header",o,[(0,a.Wm)(c,{to:"/"},{default:(0,a.w5)((()=>[(0,a._)("h1",null,[(0,a.Uk)("Zoomail "),(0,a.Wm)(l,{icon:["far","envelope"]})])])),_:1}),(0,a.Wm)(m,{status:n.props.status,onNavSWClicked:n.navSWClicked},null,8,["status","onNavSWClicked"])])}var r=t(3577);function i(e,s,t,o,n,i){return(0,a.wg)(),(0,a.iD)("button",{id:"nav-sw",onClick:s[0]||(s[0]=(...e)=>o.onClicked&&o.onClicked(...e))},[(0,a._)("span",{class:(0,r.C_)([o.props.status])},null,2)])}var l={props:{status:{required:!0,validator:e=>-1!==["menuClosed","menuOpened","detail"].indexOf(e)}},setup(e,s){const t=()=>{s.emit("navSWClicked")};return{props:e,onClicked:t}}},c=t(3744);const m=(0,c.Z)(l,[["render",i],["__scopeId","data-v-2b9e58f3"]]);var d=m,u={components:{NavSW:d},props:{status:{required:!0,validator:e=>-1!==["menuClosed","menuOpened","detail"].indexOf(e)}},setup(e,s){const t=()=>{s.emit("navSWClicked")};return{props:e,navSWClicked:t}}};const g=(0,c.Z)(u,[["render",n],["__scopeId","data-v-9fae6182"]]);var p=g},5314:function(e,s,t){"use strict";t.d(s,{Z:function(){return p}});var a=t(6252),o=t(9963),n=t(3577);const r={class:"message-wraper"},i=["onClick"];function l(e,s,t,l,c,m){return(0,a.wg)(),(0,a.iD)("div",r,[(0,a.Wm)(o.W3,{name:"message"},{default:(0,a.w5)((()=>[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)(l.displaying,(e=>((0,a.wg)(),(0,a.iD)("div",{key:e,class:(0,n.C_)(["popup-message",[l.select(e).level]])},[(0,a._)("button",{onClick:s=>l.close(e),class:"popup-close"},null,8,i),(0,a.Uk)(" "+(0,n.zw)(l.select(e).message),1)],2)))),128))])),_:1})])}var c=t(3907);const m=5e3;var d={name:"message",setup(){const e=(0,c.oR)(),s=(0,a.Fl)((()=>e.state.message.messages)),t=(0,a.Fl)((()=>{const e=Object.keys(s.value);return e.filter((e=>!s.value[e].completed&&!s.value[e].displayed))})),o=(0,a.Fl)((()=>{const e=Object.keys(s.value);return e.filter((e=>!s.value[e].completed&&s.value[e].displayed))}));(0,a.m0)((()=>{for(const s of t.value)e.commit("message/displayed",s),setTimeout((()=>{e.commit("message/completed",s)}),m)}));const n=e=>s.value[e],r=s=>e.commit("message/completed",s);return{messages:s,before_display:t,displaying:o,select:n,close:r}}},u=t(3744);const g=(0,u.Z)(d,[["render",l],["__scopeId","data-v-1e7439d2"]]);var p=g}}]);
//# sourceMappingURL=chunk-common.4d0bc642.js.map