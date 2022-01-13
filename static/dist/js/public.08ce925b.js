(function(){"use strict";var e={9858:function(e,n,t){var s=t(9963),o=t(2119),a=t(8410),l=t(1955),i={namespaced:!0,state:{messages:{}},mutations:{storeMessageFromCokie(e){const n=l.Z.get(),t=/^message_\d\d\d\d\d\d\d\d\d\d_\d\d_/,s=Object.keys(n).filter((e=>t.test(e)));for(const o of s){const s=o.replace(t,"");e.messages={...e.messages,[o]:{level:s,message:n[o],displayed:!1,completed:!1}},l.Z.remove(o)}},displayed(e,n){Object.hasOwnProperty.call(e.messages,n)&&(e.messages[n]={...e.messages[n],displayed:!0})},completed(e,n){Object.hasOwnProperty.call(e.messages,n)&&(e.messages[n]={...e.messages[n],completed:!0})},addMessage(e,n){const t=`local_${n.appname}${String(Object.keys(e.messages).length+1)}`;e.messages={...e.messages,[t]:{level:n.level,message:n.message,displayed:!1,completed:!1}}}}},r=t(6252),u=t(3577);const c={class:"container content-wraper"};function d(e,n,t,o,a,l){const i=(0,r.up)("Header"),d=(0,r.up)("router-view"),p=(0,r.up)("Footer"),m=(0,r.up)("Message");return(0,r.wg)(),(0,r.iD)("div",{id:"bg-wraper",class:(0,u.C_)({menuOpen:o.isMenuOpen,menuClose:!o.isMenuOpen})},[(0,r.Wm)(i,{onNavSWClicked:o.navSWClicked,status:o.navStatus},null,8,["onNavSWClicked","status"]),(0,r._)("main",c,[(0,r.Wm)(d,null,{default:(0,r.w5)((({Component:e})=>[(0,r.Wm)(s.uT,{mode:"out-in",name:"transition-router"},{default:(0,r.w5)((()=>[((0,r.wg)(),(0,r.j4)((0,r.LL)(e)))])),_:2},1024)])),_:1})]),(0,r.Wm)(p),(0,r.Wm)(m)],2)}var p=t(2262);const m={class:"container"},g=(0,r.Uk)("Zoomail ");function f(e,n,t,s,o,a){const l=(0,r.up)("Icon"),i=(0,r.up)("router-link"),u=(0,r.up)("NavSW");return(0,r.wg)(),(0,r.iD)("header",m,[(0,r.Wm)(i,{to:"/"},{default:(0,r.w5)((()=>[(0,r._)("h1",null,[g,(0,r.Wm)(l,{icon:["far","envelope"]})])])),_:1}),(0,r.Wm)(u,{status:s.props.status,onNavSWClicked:s.navSWClicked},null,8,["status","onNavSWClicked"])])}function v(e,n,t,s,o,a){return(0,r.wg)(),(0,r.iD)("button",{id:"nav-sw",onClick:n[0]||(n[0]=(...e)=>s.onClicked&&s.onClicked(...e))},[(0,r._)("span",{class:(0,u.C_)([s.props.status])},null,2)])}var _={props:{status:{required:!0,validator:e=>-1!==["menuClosed","menuOpened","detail"].indexOf(e)}},setup(e,n){const t=()=>{n.emit("navSWClicked")};return{props:e,onClicked:t}}},h=t(3744);const k=(0,h.Z)(_,[["render",v],["__scopeId","data-v-2b9e58f3"]]);var w=k,O={components:{NavSW:w},props:{status:{required:!0,validator:e=>-1!==["menuClosed","menuOpened","detail"].indexOf(e)}},setup(e,n){const t=()=>{n.emit("navSWClicked")};return{props:e,navSWClicked:t}}};const b=(0,h.Z)(O,[["render",f],["__scopeId","data-v-9fae6182"]]);var C=b;const W=e=>((0,r.dD)("data-v-41315f7f"),e=e(),(0,r.Cn)(),e),y={class:"container"},I=W((()=>(0,r._)("span",null," © 2019-2022 京大アンプラグド ",-1))),D={href:"https://twitter.com/ku_unplugged_hp"},S=(0,r.Uk)(" Twitter "),L={href:"https://github.com/tsume-ha/Zoomail"},M=(0,r.Uk)(" GitHub ");function j(e,n){const t=(0,r.up)("Icon");return(0,r.wg)(),(0,r.iD)("footer",y,[I,(0,r._)("a",D,[(0,r.Wm)(t,{icon:["fab","twitter"]}),S]),(0,r._)("a",L,[(0,r.Wm)(t,{icon:["fab","github"]}),M])])}const Z={},x=(0,h.Z)(Z,[["render",j],["__scopeId","data-v-41315f7f"]]);var G=x;const U={class:"message-wraper"},N=["onClick"];function F(e,n,t,o,a,l){return(0,r.wg)(),(0,r.iD)("div",U,[(0,r.Wm)(s.W3,{name:"message"},{default:(0,r.w5)((()=>[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)(o.displaying,(e=>((0,r.wg)(),(0,r.iD)("div",{key:e,class:(0,u.C_)(["popup-message",[o.select(e).level]])},[(0,r._)("button",{onClick:n=>o.close(e),class:"popup-close"},null,8,N),(0,r.Uk)(" "+(0,u.zw)(o.select(e).message),1)],2)))),128))])),_:1})])}const P=5e3;var T={name:"message",setup(){const e=(0,a.oR)(),n=(0,p.Fl)((()=>e.state.message.messages)),t=(0,p.Fl)((()=>{const e=Object.keys(n.value);return e.filter((e=>!n.value[e].completed&&!n.value[e].displayed))})),s=(0,p.Fl)((()=>{const e=Object.keys(n.value);return e.filter((e=>!n.value[e].completed&&n.value[e].displayed))}));(0,r.m0)((()=>{for(const n of t.value)e.commit("message/displayed",n),setTimeout((()=>{e.commit("message/completed",n)}),P)}));const o=e=>n.value[e],l=n=>e.commit("message/completed",n);return{messages:n,before_display:t,displaying:s,select:o,close:l}}};const H=(0,h.Z)(T,[["render",F],["__scopeId","data-v-1e7439d2"]]);var R=H,$={components:{Header:C,Footer:G,Message:R},setup(){const e=(0,o.tv)(),n=(0,a.oR)(),t=(0,p.iH)("menuClosed"),s=()=>{"menuClosed"===t.value?e.push({name:"login"}):"menuOpened"===t.value&&e.push({name:"index"})},l=(0,p.Fl)((()=>n.state.isMenuOpen));return(0,r.YP)((()=>l.value),((e,n)=>{t.value=e?"menuOpened":"menuClosed"})),{navStatus:t,isMenuOpen:l,navSWClicked:s}}};const q=(0,h.Z)($,[["render",d]]);var z=q,E=t(8947),Y=t(1436),B=t(1417),K=t(6024),X=t(7810),A=t(2001);const J=e=>((0,r.dD)("data-v-48a92981"),e=e(),(0,r.Cn)(),e),Q=J((()=>(0,r._)("div",{class:"logo-wraper"},[(0,r._)("img",{id:"logo",class:"pure-img",src:A})],-1))),V=J((()=>(0,r._)("p",null,[(0,r._)("span",null,"京都大学を中心に活動する"),(0,r._)("span",null,"アコースティック軽音サークル"),(0,r._)("br"),(0,r._)("span",null,[(0,r.Uk)("「"),(0,r._)("a",{href:"https://ku-unplugged.net",target:"_blank"},"京大アンプラグド"),(0,r.Uk)("」")]),(0,r._)("span",null,"の部内連絡管理アプリ")],-1))),ee=(0,r.Uk)("LOG IN");function ne(e,n){const t=(0,r.up)("router-link");return(0,r.wg)(),(0,r.iD)("article",null,[Q,V,(0,r.Wm)(t,{to:{name:"login"},id:"login-button",class:"btn-flat"},{default:(0,r.w5)((()=>[ee])),_:1})])}const te={},se=(0,h.Z)(te,[["render",ne],["__scopeId","data-v-48a92981"]]);var oe=se;const ae=e=>((0,r.dD)("data-v-0fdf422e"),e=e(),(0,r.Cn)(),e),le=ae((()=>(0,r._)("h2",null,"LOG IN",-1))),ie={class:"login-wraper"},re=ae((()=>(0,r._)("p",{class:"small"},[(0,r.Uk)(" Googleアカウントでログインするには事前の登録が必要です。"),(0,r._)("br"),(0,r.Uk)(" 詳しくはHP係までご連絡ください。 ")],-1))),ue=ae((()=>(0,r._)("p",{id:"login-help",class:"small"},[(0,r._)("a",{href:"/howto/",target:"_blank"},"ヘルプ：使い方へ")],-1)));function ce(e,n,t,s,o,a){const l=(0,r.up)("LoginWithLiveLog"),i=(0,r.up)("LoginWithGoogle");return(0,r.wg)(),(0,r.iD)("article",null,[le,(0,r._)("div",ie,[(0,r.Wm)(l),(0,r.Wm)(i)]),re,ue])}var de=t(3839);const pe=e=>((0,r.dD)("data-v-a667e9ec"),e=e(),(0,r.Cn)(),e),me={href:"/auth/login/auth0",class:"livelogin"},ge=pe((()=>(0,r._)("span",null,"Log in with",-1))),fe=pe((()=>(0,r._)("img",{src:de,width:"80",height:"59",alt:"LiveLog"},null,-1))),ve=[ge,fe];function _e(e,n){return(0,r.wg)(),(0,r.iD)("a",me,ve)}const he={},ke=(0,h.Z)(he,[["render",_e],["__scopeId","data-v-a667e9ec"]]);var we=ke;const Oe={href:"/auth/login/google-oauth2",id:"G-login",alt:"Sign in with Google"};function be(e,n){return(0,r.wg)(),(0,r.iD)("a",Oe," Sign in with Google ")}const Ce={},We=(0,h.Z)(Ce,[["render",be],["__scopeId","data-v-5c82dfc7"]]);var ye=We,Ie={components:{LoginWithLiveLog:we,LoginWithGoogle:ye},setup(){const e=(0,a.oR)();(0,r.bv)((()=>e.commit("message/storeMessageFromCokie")))}};const De=(0,h.Z)(Ie,[["render",ce],["__scopeId","data-v-0fdf422e"]]);var Se=De;const Le=e=>((0,r.dD)("data-v-66ff6460"),e=e(),(0,r.Cn)(),e),Me=Le((()=>(0,r._)("h2",null,"LOG OUT",-1))),je=Le((()=>(0,r._)("p",null,"ログアウトが完了しました。",-1))),Ze=(0,r.Uk)(" トップページへ ");function xe(e,n,t,s,o,a){const l=(0,r.up)("router-link");return(0,r.wg)(),(0,r.iD)("article",null,[Me,je,(0,r.Wm)(l,{to:{name:"index"},class:"btn-flat"},{default:(0,r.w5)((()=>[Ze])),_:1})])}var Ge={setup(){}};const Ue=(0,h.Z)(Ge,[["render",xe],["__scopeId","data-v-66ff6460"]]);var Ne=Ue;E.vI.add(Y.mRB,B.vnX,K.NC);const Fe=[{path:"/",name:"index",component:oe},{path:"/login/",name:"login",component:Se},{path:"/logged_out/",name:"logged_out",component:Ne}],Pe=(0,o.p7)({history:(0,o.PO)("/"),routes:Fe,base:"/"});Pe.beforeEach(((e,n,t)=>{if("/"!==e.path.slice(-1))return t(`${e.path}/`);"login"===e.name||"logged_out"===e.name?Te.commit("setIsMenuOpen",!0):Te.commit("setIsMenuOpen",!1),t()}));const Te=(0,a.MT)({strict:!1,state:{isMenuOpen:!1},mutations:{setIsMenuOpen(e,n){e.isMenuOpen=n}},modules:{message:i}});(0,s.ri)(z).use(Pe).use(Te).component("Icon",X.GN).mount("#app")},3839:function(e,n,t){e.exports=t.p+"static/dist/img/livelog.6df3ecdf.png"},2001:function(e,n,t){e.exports=t.p+"static/dist/img/zoomail.4c935cf7.png"}},n={};function t(s){var o=n[s];if(void 0!==o)return o.exports;var a=n[s]={id:s,loaded:!1,exports:{}};return e[s].call(a.exports,a,a.exports,t),a.loaded=!0,a.exports}t.m=e,function(){var e=[];t.O=function(n,s,o,a){if(!s){var l=1/0;for(c=0;c<e.length;c++){s=e[c][0],o=e[c][1],a=e[c][2];for(var i=!0,r=0;r<s.length;r++)(!1&a||l>=a)&&Object.keys(t.O).every((function(e){return t.O[e](s[r])}))?s.splice(r--,1):(i=!1,a<l&&(l=a));if(i){e.splice(c--,1);var u=o();void 0!==u&&(n=u)}}return n}a=a||0;for(var c=e.length;c>0&&e[c-1][2]>a;c--)e[c]=e[c-1];e[c]=[s,o,a]}}(),function(){t.d=function(e,n){for(var s in n)t.o(n,s)&&!t.o(e,s)&&Object.defineProperty(e,s,{enumerable:!0,get:n[s]})}}(),function(){t.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){t.o=function(e,n){return Object.prototype.hasOwnProperty.call(e,n)}}(),function(){t.nmd=function(e){return e.paths=[],e.children||(e.children=[]),e}}(),function(){t.j=501}(),function(){t.p="/"}(),function(){var e={501:0};t.O.j=function(n){return 0===e[n]};var n=function(n,s){var o,a,l=s[0],i=s[1],r=s[2],u=0;if(l.some((function(n){return 0!==e[n]}))){for(o in i)t.o(i,o)&&(t.m[o]=i[o]);if(r)var c=r(t)}for(n&&n(s);u<l.length;u++)a=l[u],t.o(e,a)&&e[a]&&e[a][0](),e[l[u]]=0;return t.O(c)},s=self["webpackChunkfront"]=self["webpackChunkfront"]||[];s.forEach(n.bind(null,0)),s.push=n.bind(null,s.push.bind(s))}();var s=t.O(void 0,[998],(function(){return t(9858)}));s=t.O(s)})();
//# sourceMappingURL=public.08ce925b.js.map