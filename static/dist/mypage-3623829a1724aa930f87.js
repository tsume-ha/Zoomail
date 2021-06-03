(window.webpackJsonp=window.webpackJsonp||[]).push([[5],{114:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("h3",[t._v("My Page")]),t._v(" "),a("p",{staticClass:"col-12 mb-3 mx-0 px-0"},[t._v("\r\n    このページでは、メーリスにおける各種設定が変更できます\r\n  ")]),t._v(" "),a("div",{staticClass:"row px-2"},[t._l(t.menuList,(function(t){return a("menulist",{key:t.header.text,attrs:{"border-color-class":t.borderColorClass,header:t.header,menu:t.menu}})})),t._v(" "),t.canRegisterDisplay?a("menulist",{key:t.registerMenu.header.text,attrs:{"border-color-class":t.registerMenu.borderColorClass,header:t.registerMenu.header,menu:t.registerMenu.menu}}):t._e(),t._v(" "),t.canAdminDisplay?a("menulist",{key:t.adminMenu.header.text,attrs:{"border-color-class":t.adminMenu.borderColorClass,header:t.adminMenu.header,menu:t.adminMenu.menu}}):t._e()],2)])};s._withStripped=!0;var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("section",{staticClass:"list-group list-group-flush col-sm-6 col-lg-4 mb-4"},[t.header.path?a("router-link",{staticClass:"list-group-item list-group-item-action border-left",class:[t.colorClass],attrs:{to:t.header.path}},[t._v("\n       "+t._s(t.header.text)+"\n   ")]):a("h6",{staticClass:"list-group-item list-group-item-action border-left disabled",class:[t.colorClass]},[t._v("\n       "+t._s(t.header.text)+"\n   ")]),t._v(" "),t._l(t.menu,(function(e){return[!1!==e.vueRouter?a("router-link",{key:e.text,staticClass:"list-group-item list-group-item-action",attrs:{to:e.path}},[t._v("\n       "+t._s(e.text)+"\n     ")]):a("a",{key:e.text,staticClass:"list-group-item list-group-item-action",attrs:{href:e.path}},[t._v("\n       "+t._s(e.text)+"\n     ")])]}))],2)};n._withStripped=!0;var r={name:"menulist",props:{borderColorClass:{required:!1,type:String},header:{required:!0,type:Object},menu:{required:!1,default:[],type:Array}},computed:{colorClass(){return["primary","secondary","success","danger","warning","info","light","dark","white"].includes(this.borderColorClass)?"border-"+this.borderColorClass:""}}},i=(a(231),a(32)),o=Object(i.a)(r,n,[],!1,null,"5dc309e8",null);o.options.__file="front/components/mypage/menulist.vue";var l={name:"mypage-index",components:{menulist:o.exports},data:()=>({menuList:[{borderColorClass:"info",header:{text:"登録情報"},menu:[{text:"登録情報変更",path:"./info-update/"},{text:"メーリス受信設定",path:"./mail-settings/"},{text:"メーリス受信テスト",path:"./mail-test/"},{text:"LiveLog・Google認証",path:"./oauth/"}]},{borderColorClass:"secondary",header:{text:"ログアウト"},menu:[{text:"ログアウトする",path:"/logout/",vueRouter:!1}]}],adminMenu:{borderColorClass:"danger",header:{text:"管理サイト"},menu:[{text:"DB管理サイト",path:"/admin/",vueRouter:!1}]},registerMenu:{borderColorClass:"warning",header:{text:"ユーザー登録"},menu:[{text:"ユーザー登録フォーム",path:"./register/"}]}}),created(){this.$store.dispatch("members/getUserInfo")},computed:{user(){return this.$store.state.members.user},canAdminDisplay(){return!(!this.user||!this.user.permissions||!this.user.permissions.is_admin&&!this.user.permissions.is_superuser)},canRegisterDisplay(){return!(!this.user||!this.user.permissions||!this.user.permissions.can_register_user&&!this.user.permissions.is_superuser)}}},m=Object(i.a)(l,s,[],!1,null,null,null);m.options.__file="front/components/mypage/index.vue";e.default=m.exports},120:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("h3",[t._v("LiveLog・Google認証")]),t._v(" "),a("section",[a("p",[t._v("認証を行ったサービスのアカウントでログインすることが出来ます。")]),t._v(" "),a("table",{staticClass:"table"},[a("tbody",[a("tr",[a("td",[t._v("Google")]),t._v(" "),a("td",[t.google?a("span",{staticClass:"text-success"},[t._v("認証しています")]):a("a",{attrs:{href:"/auth/login/google-oauth2?next=/mypage/oauth/"}},[t._v("認証する")])]),t._v(" "),t.canUnlink?a("td",[a("a",{staticClass:"text-warning",on:{click:t.onclicked}},[t._v("紐付けを解除する")])]):t.needLivelogLogin?a("td",[a("span",[t._v("紐付けを解除するまえに、もう一度LiveLogへログインしてください")])]):t._e()]),t._v(" "),a("tr",[a("td",[t._v("LiveLog")]),t._v(" "),a("td",[t.livelog?a("span",{staticClass:"text-success"},[t._v("認証しています")]):a("a",{attrs:{href:"/auth/login/auth0?next=/mypage/oauth/"}},[t._v("\n            認証する\n          ")])]),t._v(" "),t.canUnlink?a("td"):t.needLivelogLogin?a("td",[a("a",{attrs:{href:"/auth/login/auth0?next=/mypage/oauth/"}},[t._v("\n            LiveLogにログイン\n          ")])]):t._e()])])]),t._v(" "),a("router-link",{staticClass:"btn btn-secondary mr-4",attrs:{to:"../"}},[t._v("戻る")])],1),t._v(" "),t.nowloading?a("nowloading",{attrs:{text:"通信中です..."}}):t._e()],1)};s._withStripped=!0;var n={name:"mypage-oauth",metaInfo:{title:"LiveLog・Google認証"},components:{nowloading:a(127).a},created(){this.$store.dispatch("members/getUserInfo")},data:()=>({nowloading:!1}),computed:{userInfo(){return this.$store.state.members.user},google(){return this.userInfo.google_oauth2},livelog(){return this.userInfo.livelog_auth0},hasLivelogEmail(){return Boolean(this.userInfo.livelog_email)},canUnlink(){return this.google&&this.livelog&&this.hasLivelogEmail},needLivelogLogin(){return this.google&&this.livelog&&!this.hasLivelogEmail}},methods:{onclicked(){this.nowloading=!0,this.axios.post("/api/mypage/google_unlink/",{unlink:!0}).then(t=>{t.data.deleted?this.$toast.success("Gogleアカウントの紐付けを解除しました"):this.$toast.warning("Gogleアカウントの紐付けを解除ができませんでした。お手数ですが開発者までお問い合わせください")}).catch(t=>{console.log(t.response.data),t.response.data&&"message"in t.response.data&&this.$toast.error(t.response.data.message,{duration:5e3}),this.$toast.error("処理が完了しませんでした。",{duration:5e3})}).finally(()=>{this.$store.dispatch("members/getUserInfo"),this.nowloading=!1})}}},r=a(32),i=Object(r.a)(n,s,[],!1,null,null,null);i.options.__file="front/components/mypage/oauth.vue";e.default=i.exports},121:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("h3",[t._v("登録情報変更")]),t._v(" "),a("section",[a("p",{staticClass:"small my-2"},[t._v("\n    メールアドレス関係の設定は\n    "),a("router-link",{attrs:{to:"/mypage/mail-settings/"}},[t._v("こちら")]),t._v("\n    に移行しました\n  ")],1),t._v(" "),a("form",[a("div",{staticClass:"form-group"},[a("label",{attrs:{for:"id_last_name"}},[t._v("名字:")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.last_name,expression:"formData.last_name"}],staticClass:"form-control",attrs:{type:"text",name:"last_name",maxlength:"255",required:"",id:"id_last_name"},domProps:{value:t.formData.last_name},on:{input:function(e){e.target.composing||t.$set(t.formData,"last_name",e.target.value)}}})]),t._v(" "),a("div",{staticClass:"form-group"},[a("label",{attrs:{for:"id_first_name"}},[t._v("名前:")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.first_name,expression:"formData.first_name"}],staticClass:"form-control",attrs:{type:"text",name:"first_name",maxlength:"255",required:"",id:"id_first_name"},domProps:{value:t.formData.first_name},on:{input:function(e){e.target.composing||t.$set(t.formData,"first_name",e.target.value)}}})]),t._v(" "),a("div",{staticClass:"form-group"},[a("label",{attrs:{for:"id_furigana"}},[t._v("ふりがな:")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.furigana,expression:"formData.furigana"}],staticClass:"form-control",attrs:{type:"text",name:"furigana",maxlength:"255",required:"",id:"id_furigana"},domProps:{value:t.formData.furigana},on:{input:function(e){e.target.composing||t.$set(t.formData,"furigana",e.target.value)}}})]),t._v(" "),a("div",{staticClass:"form-group"},[a("label",{attrs:{for:"id_nickname"}},[t._v("ニックネーム:")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.nickname,expression:"formData.nickname"}],staticClass:"form-control",attrs:{type:"text",name:"nickname",maxlength:"255",id:"id_nickname"},domProps:{value:t.formData.nickname},on:{input:function(e){e.target.composing||t.$set(t.formData,"nickname",e.target.value)}}})]),t._v(" "),a("router-link",{staticClass:"btn btn-secondary mx-2 my-3",attrs:{to:"../"}},[t._v("戻る")]),t._v(" "),a("button",{staticClass:"btn btn-info mx-2 my-3",on:{click:function(e){return e.preventDefault(),t.onclicked(e)}}},[t._v("\n      更新\n    ")])],1)]),t._v(" "),t.nowloading?a("nowloading",{attrs:{text:"通信中です..."}}):t._e()],1)};s._withStripped=!0;var n={name:"mypage-info-update",components:{nowloading:a(127).a},metaInfo:{title:"登録情報変更"},created(){this.nowloading=!0,this.$store.dispatch("members/getUserInfo").then(()=>{this.nowloading=!1,this.$set(this.formData,"last_name",this.userInfo.last_name),this.$set(this.formData,"first_name",this.userInfo.first_name),this.$set(this.formData,"furigana",this.userInfo.furigana),this.$set(this.formData,"nickname",this.userInfo.nickname)}).catch(t=>{nowloading=!1,console.log(t)})},data:()=>({nowloading:!1,formData:{last_name:"",first_name:"",furigana:"",nickname:""}}),computed:{userInfo(){return this.$store.state.members.user}},methods:{onclicked(){this.nowloading=!0,this.axios.post("/api/mypage/info-update/",this.formData).then(t=>{if(!0===t.data.successed)this.$toast.success("更新しました");else for(const e of t.data.messages)this.$toast.error(e,{duration:5e3})}).finally(()=>{this.$store.dispatch("members/getUserInfo"),this.nowloading=!1})}}},r=a(32),i=Object(r.a)(n,s,[],!1,null,null,null);i.options.__file="front/components/mypage/info-update.vue";e.default=i.exports},122:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("h3",[t._v("メーリス受信設定")]),t._v(" "),a("section",[a("form",[a("div",{staticClass:"form-group"},[a("label",{attrs:{for:"id_last_name"}},[t._v("受信用メールアドレス:")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.receive_email,expression:"formData.receive_email"}],staticClass:"form-control",attrs:{type:"email",name:"last_name",maxlength:"254",required:"false",id:"id_last_name"},domProps:{value:t.formData.receive_email},on:{input:function(e){e.target.composing||t.$set(t.formData,"receive_email",e.target.value)}}}),t._v(" "),t._m(0)]),t._v(" "),a("div",{staticClass:"form-group"},[a("label",{attrs:{for:"id_send_mail"}},[t._v("メーリスを受信する:")]),t._v(" "),a("input",{directives:[{name:"model",rawName:"v-model",value:t.formData.send_mail,expression:"formData.send_mail"}],staticClass:"mx-2",attrs:{type:"checkbox",name:"send_mail",id:"id_send_mail"},domProps:{checked:Array.isArray(t.formData.send_mail)?t._i(t.formData.send_mail,null)>-1:t.formData.send_mail},on:{change:function(e){var a=t.formData.send_mail,s=e.target,n=!!s.checked;if(Array.isArray(a)){var r=t._i(a,null);s.checked?r<0&&t.$set(t.formData,"send_mail",a.concat([null])):r>-1&&t.$set(t.formData,"send_mail",a.slice(0,r).concat(a.slice(r+1)))}else t.$set(t.formData,"send_mail",n)}}}),t._v(" "),t._m(1)]),t._v(" "),a("router-link",{staticClass:"btn btn-secondary mx-2 my-3",attrs:{to:"../"}},[t._v("戻る")]),t._v(" "),a("button",{staticClass:"btn btn-info mx-2 my-3",on:{click:function(e){return e.preventDefault(),t.onclicked(e)}}},[t._v("\n      更新\n    ")])],1)]),t._v(" "),t.nowloading?a("nowloading",{attrs:{text:"通信中です..."}}):t._e()],1)};s._withStripped=!0;var n={name:"mypage-mail-settings",components:{nowloading:a(127).a},metaInfo:{title:"メーリス受信設定"},created(){this.nowloading=!0,this.$store.dispatch("members/getUserInfo").then(()=>{this.nowloading=!1,this.$set(this.formData,"receive_email",this.userInfo.receive_email),this.$set(this.formData,"send_mail",this.userInfo.send_mail)}).catch(t=>{nowloading=!1,console.log(t)})},data:()=>({nowloading:!1,formData:{receive_email:"",send_mail:!0}}),computed:{userInfo(){return this.$store.state.members.user}},methods:{onclicked(){this.nowloading=!0,this.axios.post("/api/mypage/mail-settings/",this.formData).then(t=>{if(!0===t.data.successed)this.$toast.success("更新しました");else for(const e of t.data.messages)this.$toast.error(e,{duration:5e3})}).finally(()=>{this.$store.dispatch("members/getUserInfo").then(()=>{this.nowloading=!1,this.$set(this.formData,"receive_email",this.userInfo.receive_email),this.$set(this.formData,"send_mail",this.userInfo.send_mail)})})}}},r=a(32),i=Object(r.a)(n,s,[function(){var t=this.$createElement,e=this._self._c||t;return e("p",{staticClass:"small text-secondary"},[this._v("\n        メーリスを受信するメールアドレスを指定してください。"),e("br"),this._v("\n        空白の場合は、ログインに用いるGmailアドレスか、\n        LiveLogアカウントに登録されたメールアドレスになります。\n      ")])},function(){var t=this.$createElement,e=this._self._c||t;return e("p",{staticClass:"small text-secondary"},[this._v("\n          メーリスを受け取りたくない場合はチェックを外してください。"),e("br"),this._v("\n          チェックが外されると、全回・回生メーリスともに送信されないようになりますが、"),e("br"),this._v("\n          このサイトにログインし、メーリスを確認することは出来ます。\n      ")])}],!1,null,null,null);i.options.__file="front/components/mypage/mail-settings.vue";e.default=i.exports},123:function(t,e,a){"use strict";a.r(e);var s=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("h3",[t._v("メール受信テスト")]),t._v(" "),a("section",[a("div",{staticClass:"mt-4 mb-2"},[a("span",{staticClass:"mb-2"},[t._v("現在設定されているメールアドレス")]),t._v(" "),a("br"),t._v(" "),t.showEmailAddress?a("span",[t._v("\n      "+t._s(t.userInfo.receive_email)+"\n    ")]):a("span",[t._v("\n      ******************\n    ")])]),t._v(" "),a("div",{staticClass:"mb-3"},[t.showEmailAddress?a("button",{staticClass:"btn btn-sm btn-light",on:{click:function(e){t.showEmailAddress=!1}}},[t._v("メールアドレスを隠す")]):a("button",{staticClass:"btn btn-sm btn-light",on:{click:function(e){t.showEmailAddress=!0}}},[t._v("メールアドレスを表示する")])]),t._v(" "),t._m(0),t._v(" "),a("router-link",{staticClass:"btn btn-secondary mx-2 my-3",attrs:{to:"../"}},[t._v("戻る")]),t._v(" "),a("button",{staticClass:"btn btn-info mx-2 my-3",on:{click:function(e){return e.preventDefault(),t.onclicked(e)}}},[t._v("\n    送信する\n  ")])],1),t._v(" "),t.nowloading?a("nowloading",{attrs:{text:"通信中です..."}}):t._e()],1)};s._withStripped=!0;var n={name:"mypage-mail-test",components:{nowloading:a(127).a},metaInfo:{title:"メール受信テスト"},created(){this.$store.dispatch("members/getUserInfo")},data:()=>({nowloading:!1,showEmailAddress:!1}),computed:{userInfo(){return this.$store.state.members.user}},methods:{onclicked(){if(!window.confirm("送信しますか？"))return!1;this.nowloading=!0,this.axios.post("/api/mypage/mail-test/",{send:"true"}).then(t=>{console.log(t),this.$toast.success("送信しました")}).catch(t=>{console.log(t),400==t.response.status?this.$toast.error("送信できませんでした。通信環境を確認してもう一度試してみてください。",{duration:5e3}):429==t.response.status&&this.$toast.warning("送信は5分に1回のみ可能です。時間をおいて再度アクセスしてください。",{duration:5e3})}).finally(()=>{this.nowloading=!1})}}},r=a(32),i=Object(r.a)(n,s,[function(){var t=this.$createElement,e=this._self._c||t;return e("p",{staticClass:"small"},[this._v("\n    メーリスがきちんと受信できるか確かめるために、テストメールを送信します。"),e("br"),this._v("\n    テストメールの送信は5分に1回行うことができます。\n  ")])}],!1,null,null,null);i.options.__file="front/components/mypage/mail-test.vue";e.default=i.exports},126:function(t,e,a){var s=a(129);"string"==typeof s&&(s=[[t.i,s,""]]),s.locals&&(t.exports=s.locals);(0,a(48).default)("cc4c5b38",s,!1,{})},127:function(t,e,a){"use strict";var s=function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticClass:"wrap"},[e("div",{staticClass:"innner-wrap"},[e("span",{staticClass:"rotate"}),e("br"),this._v(" "),e("span",{staticClass:"text"},[this._v(this._s(this.text))])])])};s._withStripped=!0;var n={name:"nowloading",props:{text:{required:!1,type:String,default:""}}},r=(a(128),a(32)),i=Object(r.a)(n,s,[],!1,null,"fc97438a",null);i.options.__file="front/components/nowloading.vue";e.a=i.exports},128:function(t,e,a){"use strict";var s=a(126);a.n(s).a},129:function(t,e,a){(e=a(47)(!1)).push([t.i,"\ndiv.wrap[data-v-fc97438a]{\r\n  position: fixed;\r\n  display: flex;\r\n  justify-content: center;\r\n  align-items: center;\r\n  text-align: center;\r\n  top: 0;\r\n  left: 0;\r\n  margin: 0;\r\n  padding: 0;\r\n  width: 100vw;\r\n  height: 100vh;\r\n  z-index: 1000;\r\n  background-color: rgba(255, 255, 255, 0.7);\n}\ndiv.inner-wrap[data-v-fc97438a]{\r\n  position: relative;\r\n  text-align: center;\r\n  width: 200px;\n}\nspan.rotate[data-v-fc97438a]{\r\n  width: 60px;\r\n  height: 60px;\r\n  display: inline-block;\r\n  position: relative;\r\n  border-top: 8px #31b1e4 solid;\r\n  border-right: 8px #31b1e4 solid;\r\n  border-bottom: 8px #31b1e4 solid;\r\n  border-left: 8px transparent solid;\r\n  border-radius: 50%;\r\n  animation: 1s linear infinite rotation-data-v-fc97438a;\n}\n@keyframes rotation-data-v-fc97438a{\n0%{ transform:rotate(0);}\n100%{ transform:rotate(360deg);\n}\n}\nspan.text[data-v-fc97438a]{\r\n  text-shadow: 0 0 10px #fff ;\n}\r\n\r\n",""]),t.exports=e},162:function(t,e,a){var s=a(232);"string"==typeof s&&(s=[[t.i,s,""]]),s.locals&&(t.exports=s.locals);(0,a(48).default)("4ac1c785",s,!1,{})},231:function(t,e,a){"use strict";var s=a(162);a.n(s).a},232:function(t,e,a){(e=a(47)(!1)).push([t.i,"\nsection[data-v-5dc309e8] :first-child{\r\n  font-size: 1.25rem;\r\n  color: #212529 !important;\r\n  border-top: none;\r\n  border-left-width: 0.5rem!important;\r\n  padding-left: 0.75rem;\n}\nsection[data-v-5dc309e8] :last-child{\r\n  border-bottom: 1px solid rgba(0,0,0,.125) !important;\n}\r\n",""]),t.exports=e}}]);