(function(){"use strict";var n={5305:function(n,e,t){var o=t(9963),r=t(2201),i=t(3907),a=t(114),u=t(6252),l=t(3577);const s={class:"container content-wraper"};function c(n,e,t,r,i,a){const c=(0,u.up)("Header"),d=(0,u.up)("router-view"),p=(0,u.up)("Footer"),f=(0,u.up)("Message");return(0,u.wg)(),(0,u.iD)("div",{id:"bg-wraper",class:(0,l.C_)({menuOpen:r.isMenuOpen,menuClose:!r.isMenuOpen})},[(0,u.Wm)(c,{onNavSWClicked:r.navSWClicked,status:r.navStatus},null,8,["onNavSWClicked","status"]),(0,u._)("main",s,[(0,u.Wm)(d,null,{default:(0,u.w5)((({Component:n})=>[(0,u.Wm)(o.uT,{mode:"out-in",name:"transition-router"},{default:(0,u.w5)((()=>[((0,u.wg)(),(0,u.j4)((0,u.LL)(n)))])),_:2},1024)])),_:1})]),(0,u.Wm)(p),(0,u.Wm)(f)],2)}t(7658);var d=t(2262),p=t(8337),f=t(1542),g=t(5314),m={components:{Header:p.Z,Footer:f.Z,Message:g.Z},setup(){const n=(0,r.tv)(),e=(0,i.oR)(),t=(0,d.iH)("menuClosed"),o=()=>{"menuClosed"===t.value?n.push({name:"login"}):"menuOpened"===t.value&&n.push({name:"index"})},a=(0,u.Fl)((()=>e.state.isMenuOpen));return(0,u.YP)((()=>a.value),((n,e)=>{t.value=n?"menuOpened":"menuClosed"})),{navStatus:t,isMenuOpen:a,navSWClicked:o}}},v=t(3744);const h=(0,v.Z)(m,[["render",c]]);var _=h,O=t(3636),b=t(9417),w=t(3024),k=t(4288),C=t(7810),W=t.p+"static/dist/img/zoomail.4c935cf7.png";const L=n=>((0,u.dD)("data-v-4655fc13"),n=n(),(0,u.Cn)(),n),M=L((()=>(0,u._)("div",{class:"logo-wraper"},[(0,u._)("img",{id:"logo",class:"pure-img",src:W})],-1))),y=L((()=>(0,u._)("p",null,[(0,u._)("span",null,"京都大学を中心に活動する"),(0,u._)("span",null,"アコースティック軽音サークル"),(0,u._)("br"),(0,u._)("span",null,[(0,u.Uk)("「"),(0,u._)("a",{href:"https://ku-unplugged.net",target:"_blank"},"京大アンプラグド"),(0,u.Uk)("」")]),(0,u._)("span",null,"の部内連絡管理アプリ")],-1)));function S(n,e){const t=(0,u.up)("router-link");return(0,u.wg)(),(0,u.iD)("article",null,[M,y,(0,u.Wm)(t,{to:{name:"login"},id:"login-button",class:"btn-flat"},{default:(0,u.w5)((()=>[(0,u.Uk)("LOG IN")])),_:1})])}const I={},j=(0,v.Z)(I,[["render",S],["__scopeId","data-v-4655fc13"]]);var D=j;const G=n=>((0,u.dD)("data-v-0fdf422e"),n=n(),(0,u.Cn)(),n),Z=G((()=>(0,u._)("h2",null,"LOG IN",-1))),x={class:"login-wraper"},P=G((()=>(0,u._)("p",{class:"small"},[(0,u.Uk)(" Googleアカウントでログインするには事前の登録が必要です。"),(0,u._)("br"),(0,u.Uk)(" 詳しくはHP係までご連絡ください。 ")],-1))),T=G((()=>(0,u._)("p",{id:"login-help",class:"small"},[(0,u._)("a",{href:"/howto/",target:"_blank"},"ヘルプ：使い方へ")],-1)));function U(n,e,t,o,r,i){const a=(0,u.up)("LoginWithLiveLog"),l=(0,u.up)("LoginWithGoogle");return(0,u.wg)(),(0,u.iD)("article",null,[Z,(0,u._)("div",x,[(0,u.Wm)(a),(0,u.Wm)(l)]),P,T])}var N=t.p+"static/dist/img/livelog.6df3ecdf.png";const F=n=>((0,u.dD)("data-v-a667e9ec"),n=n(),(0,u.Cn)(),n),H={href:"/auth/login/auth0",class:"livelogin"},R=F((()=>(0,u._)("span",null,"Log in with",-1))),E=F((()=>(0,u._)("img",{src:N,width:"80",height:"59",alt:"LiveLog"},null,-1))),z=[R,E];function B(n,e){return(0,u.wg)(),(0,u.iD)("a",H,z)}const V={},X=(0,v.Z)(V,[["render",B],["__scopeId","data-v-a667e9ec"]]);var Y=X;const $={href:"/auth/login/google-oauth2",id:"G-login",alt:"Sign in with Google"};function q(n,e){return(0,u.wg)(),(0,u.iD)("a",$," Sign in with Google ")}const A={},J=(0,v.Z)(A,[["render",q],["__scopeId","data-v-5c82dfc7"]]);var K=J,Q={components:{LoginWithLiveLog:Y,LoginWithGoogle:K},setup(){const n=(0,i.oR)();(0,u.bv)((()=>n.commit("message/storeMessageFromCokie")))}};const nn=(0,v.Z)(Q,[["render",U],["__scopeId","data-v-0fdf422e"]]);var en=nn;const tn=n=>((0,u.dD)("data-v-66ff6460"),n=n(),(0,u.Cn)(),n),on=tn((()=>(0,u._)("h2",null,"LOG OUT",-1))),rn=tn((()=>(0,u._)("p",null,"ログアウトが完了しました。",-1)));function an(n,e,t,o,r,i){const a=(0,u.up)("router-link");return(0,u.wg)(),(0,u.iD)("article",null,[on,rn,(0,u.Wm)(a,{to:{name:"index"},class:"btn-flat"},{default:(0,u.w5)((()=>[(0,u.Uk)(" トップページへ ")])),_:1})])}var un={setup(){}};const ln=(0,v.Z)(un,[["render",an],["__scopeId","data-v-66ff6460"]]);var sn=ln;O.vI.add(b.mRB,w.vnX,k.NCV);const cn=[{path:"/",name:"index",component:D},{path:"/login/",name:"login",component:en},{path:"/logged_out/",name:"logged_out",component:sn}],dn=(0,r.p7)({history:(0,r.PO)("/"),routes:cn,base:"/"});dn.beforeEach(((n,e,t)=>{if("/"!==n.path.slice(-1))return t(`${n.path}/`);"login"===n.name||"logged_out"===n.name?pn.commit("setIsMenuOpen",!0):pn.commit("setIsMenuOpen",!1),t()}));const pn=(0,i.MT)({strict:!1,state:{isMenuOpen:!1},mutations:{setIsMenuOpen(n,e){n.isMenuOpen=e}},modules:{message:a.Z}});(0,o.ri)(_).use(dn).use(pn).component("Icon",C.GN).mount("#app")}},e={};function t(o){var r=e[o];if(void 0!==r)return r.exports;var i=e[o]={id:o,loaded:!1,exports:{}};return n[o].call(i.exports,i,i.exports,t),i.loaded=!0,i.exports}t.m=n,function(){var n=[];t.O=function(e,o,r,i){if(!o){var a=1/0;for(c=0;c<n.length;c++){o=n[c][0],r=n[c][1],i=n[c][2];for(var u=!0,l=0;l<o.length;l++)(!1&i||a>=i)&&Object.keys(t.O).every((function(n){return t.O[n](o[l])}))?o.splice(l--,1):(u=!1,i<a&&(a=i));if(u){n.splice(c--,1);var s=r();void 0!==s&&(e=s)}}return e}i=i||0;for(var c=n.length;c>0&&n[c-1][2]>i;c--)n[c]=n[c-1];n[c]=[o,r,i]}}(),function(){t.n=function(n){var e=n&&n.__esModule?function(){return n["default"]}:function(){return n};return t.d(e,{a:e}),e}}(),function(){t.d=function(n,e){for(var o in e)t.o(e,o)&&!t.o(n,o)&&Object.defineProperty(n,o,{enumerable:!0,get:e[o]})}}(),function(){t.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(n){if("object"===typeof window)return window}}()}(),function(){t.o=function(n,e){return Object.prototype.hasOwnProperty.call(n,e)}}(),function(){t.r=function(n){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(n,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(n,"__esModule",{value:!0})}}(),function(){t.nmd=function(n){return n.paths=[],n.children||(n.children=[]),n}}(),function(){t.j=501}(),function(){t.p="/"}(),function(){var n={501:0};t.O.j=function(e){return 0===n[e]};var e=function(e,o){var r,i,a=o[0],u=o[1],l=o[2],s=0;if(a.some((function(e){return 0!==n[e]}))){for(r in u)t.o(u,r)&&(t.m[r]=u[r]);if(l)var c=l(t)}for(e&&e(o);s<a.length;s++)i=a[s],t.o(n,i)&&n[i]&&n[i][0](),n[i]=0;return t.O(c)},o=self["webpackChunkfront"]=self["webpackChunkfront"]||[];o.forEach(e.bind(null,0)),o.push=e.bind(null,o.push.bind(o))}();var o=t.O(void 0,[998,64],(function(){return t(5305)}));o=t.O(o)})();
//# sourceMappingURL=public.3ca3bb33.js.map