(function(){"use strict";var e={6874:function(e,a,n){var t=n(9963),l=n(6252),r=n(2262),i=n(2369),s=n.n(i),u=n(8337),o=n(1542),m=n(3577);const c=["textContent"];function p(e,a,n,t,r,i){return(0,l.wg)(),(0,l.iD)("ul",null,[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)(n.messages,(e=>((0,l.wg)(),(0,l.iD)("li",{key:e,textContent:(0,m.zw)(e)},null,8,c)))),128))])}var d={name:"validation-error-messages",props:{messages:{required:!0,type:Array}}},f=n(3744);const g=(0,f.Z)(d,[["render",p],["__scopeId","data-v-12ab29c6"]]);var v=g,_=n(8042);const h=e=>((0,l.dD)("data-v-4586757e"),e=e(),(0,l.Cn)(),e),y={class:"container"},k=(0,l.uE)("<h2 data-v-4586757e>Zoomailへようこそ！</h2><p data-v-4586757e><em data-v-4586757e>Zoomail</em>は、京大アンプラグドの<em data-v-4586757e>メール配信プラットフォーム</em>です。<br data-v-4586757e> このZoomailを通して、皆さんにはサークルの全体連絡である<em data-v-4586757e>メーリス</em>が届きます。<br data-v-4586757e> 日常的な連絡はSlackで行われますが、Zoomailからは<em data-v-4586757e>ライブの告知</em>や<em data-v-4586757e>合宿のお知らせ</em>、<em data-v-4586757e>会費の振り込み</em>など、<em data-v-4586757e>サークル運営にかかわる重要な連絡</em>が送られてきます！ </p><p data-v-4586757e>このフォームにメールアドレスを登録して、メーリスを受信しましょう</p>",3),b={class:"pure-control-group"},w=h((()=>(0,l._)("label",{for:"id_email"},"メールアドレス:",-1))),N=h((()=>(0,l._)("p",{class:"small"},[(0,l.Uk)("このメールアドレスにメーリスが届きます。"),(0,l._)("br"),(0,l.Uk)("LiveLogに登録したものと異なるメールアドレスでも受信可能です。")],-1))),x={class:"pure-control-group"},j=h((()=>(0,l._)("label",{for:"id_last_name"},"苗字:",-1))),O={class:"pure-control-group"},q=h((()=>(0,l._)("label",{for:"id_first_name"},"名前:",-1))),Z={class:"pure-control-group"},U=h((()=>(0,l._)("label",{for:"id_furigana"},"ふりがな:",-1))),S=h((()=>(0,l._)("p",{class:"small"},"ひらがなのみ（五十音順のソートに使われます）",-1))),C={class:"pure-control-group"},D=h((()=>(0,l._)("label",{for:"id_nickname"},"ニックネーム:",-1))),V=h((()=>(0,l._)("p",{class:"small"},"メーリスを送信するときの表示名になります",-1))),H=h((()=>(0,l._)("div",{class:"pure-controls"},[(0,l._)("button",{type:"submit",class:"pure-button button-primary"},"登録する！")],-1)));var I={__name:"FirstRegisterApp",setup(e){const a=(0,r.iH)(!0),n=(0,r.qj)({email:"",lastName:"",firstName:"",furigana:"",nickname:""}),i=(0,r.iH)({});(()=>{_.Z.get("/api/tempuser/").then((e=>{n.email=e?.data?.email?e.data.email:"",n.lastName=e?.data?.lastName?e.data.lastName:"",n.firstName=e?.data?.firstName?e.data.firstName:"",n.furigana=e?.data?.furigana?e.data.furigana:"",n.nickname=e?.data?.nickname?e.data.nickname:""})).finally((()=>{a.value=!1}))})();const m=e=>{e.preventDefault(),a.value=!0;const t=new FormData;t.append("email",n.email),t.append("last_name",n.lastName),t.append("first_name",n.firstName),t.append("furigana",n.furigana),t.append("nickname",n.nickname),_.Z.post("/api/first-register/",t).then((()=>{a.value=!1,location.replace("/")})).catch((e=>{console.error(e),400===e.response.status&&(i.value={...e.response.data})})).finally((()=>{a.value=!1}))};return(e,c)=>((0,l.wg)(),(0,l.iD)(l.HY,null,[(0,l.Wm)(u.Z,{status:"menuClosed"}),(0,l._)("main",y,[(0,l._)("article",null,[k,(0,l._)("form",{onSubmit:m,class:"pure-form pure-form-stacked"},[(0,l._)("div",b,[w,(0,l.wy)((0,l._)("input",{type:"email",name:"email","onUpdate:modelValue":c[0]||(c[0]=e=>n.email=e),maxlength:"255",required:"",id:"id_email",class:"pure-input-1"},null,512),[[t.nr,n.email]]),N,i.value?.email?.length?((0,l.wg)(),(0,l.j4)(v,{key:0,messages:i.value.email.map((e=>e.message))},null,8,["messages"])):(0,l.kq)("",!0)]),(0,l._)("div",x,[j,(0,l.wy)((0,l._)("input",{type:"text",name:"last_name","onUpdate:modelValue":c[1]||(c[1]=e=>n.lastName=e),maxlength:"255",required:"",placeholder:"京大",id:"id_last_name",class:"pure-input-1"},null,512),[[t.nr,n.lastName]]),i.value?.lastName?.length?((0,l.wg)(),(0,l.j4)(v,{key:0,messages:i.value.lastName.map((e=>e.message))},null,8,["messages"])):(0,l.kq)("",!0)]),(0,l._)("div",O,[q,(0,l.wy)((0,l._)("input",{type:"text",name:"first_name","onUpdate:modelValue":c[2]||(c[2]=e=>n.firstName=e),maxlength:"255",required:"",placeholder:"太郎",id:"id_first_name",class:"pure-input-1"},null,512),[[t.nr,n.firstName]]),i.value?.firstName?.length?((0,l.wg)(),(0,l.j4)(v,{key:0,messages:i.value.firstName.map((e=>e.message))},null,8,["messages"])):(0,l.kq)("",!0)]),(0,l._)("div",Z,[U,(0,l.wy)((0,l._)("input",{type:"text",name:"furigana","onUpdate:modelValue":c[3]||(c[3]=e=>n.furigana=e),maxlength:"255",required:"",placeholder:"きょうだいたろう",id:"id_furigana",class:"pure-input-1"},null,512),[[t.nr,n.furigana]]),S,i.value?.furigana?.length?((0,l.wg)(),(0,l.j4)(v,{key:0,messages:i.value.furigana.map((e=>e.message))},null,8,["messages"])):(0,l.kq)("",!0)]),(0,l._)("div",C,[D,(0,l.wy)((0,l._)("input",{type:"text",name:"nickname","onUpdate:modelValue":c[4]||(c[4]=e=>n.nickname=e),maxlength:"255",placeholder:"たろー",id:"id_nickname",class:"pure-input-1"},null,512),[[t.nr,n.nickname]]),V,i.value?.nickname?.length?((0,l.wg)(),(0,l.j4)(v,{key:0,messages:i.value.nickname.map((e=>e.message))},null,8,["messages"])):(0,l.kq)("",!0)]),H],32)])]),(0,l.Wm)(o.Z),(0,l.Wm)((0,r.SU)(s()),{active:a.value,"onUpdate:active":c[5]||(c[5]=e=>a.value=e),"can-cancel":!1,"is-full-page":!0,color:"#386471"},null,8,["active"])],64))}};const P=(0,f.Z)(I,[["__scopeId","data-v-4586757e"]]);var T=P,F=n(3636),M=n(9417),W=n(3024),A=n(4288),E=n(7810);F.vI.add(M.mRB,W.vnX,A.NCV),(0,t.ri)(T).component("Icon",E.GN).mount("#app")}},a={};function n(t){var l=a[t];if(void 0!==l)return l.exports;var r=a[t]={id:t,loaded:!1,exports:{}};return e[t].call(r.exports,r,r.exports,n),r.loaded=!0,r.exports}n.m=e,function(){var e=[];n.O=function(a,t,l,r){if(!t){var i=1/0;for(m=0;m<e.length;m++){t=e[m][0],l=e[m][1],r=e[m][2];for(var s=!0,u=0;u<t.length;u++)(!1&r||i>=r)&&Object.keys(n.O).every((function(e){return n.O[e](t[u])}))?t.splice(u--,1):(s=!1,r<i&&(i=r));if(s){e.splice(m--,1);var o=l();void 0!==o&&(a=o)}}return a}r=r||0;for(var m=e.length;m>0&&e[m-1][2]>r;m--)e[m]=e[m-1];e[m]=[t,l,r]}}(),function(){n.n=function(e){var a=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(a,{a:a}),a}}(),function(){n.d=function(e,a){for(var t in a)n.o(a,t)&&!n.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:a[t]})}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,a){return Object.prototype.hasOwnProperty.call(e,a)}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.nmd=function(e){return e.paths=[],e.children||(e.children=[]),e}}(),function(){n.j=341}(),function(){var e={341:0};n.O.j=function(a){return 0===e[a]};var a=function(a,t){var l,r,i=t[0],s=t[1],u=t[2],o=0;if(i.some((function(a){return 0!==e[a]}))){for(l in s)n.o(s,l)&&(n.m[l]=s[l]);if(u)var m=u(n)}for(a&&a(t);o<i.length;o++)r=i[o],n.o(e,r)&&e[r]&&e[r][0](),e[r]=0;return n.O(m)},t=self["webpackChunkfront"]=self["webpackChunkfront"]||[];t.forEach(a.bind(null,0)),t.push=a.bind(null,t.push.bind(t))}();var t=n.O(void 0,[998,64],(function(){return n(6874)}));t=n.O(t)})();
//# sourceMappingURL=first_register.a065945d.js.map