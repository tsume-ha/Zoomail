(window.webpackJsonp=window.webpackJsonp||[]).push([[1],{161:function(t,e,s){"use strict";s.r(e);var a=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("h3",[t._v("メーリス一覧")]),t._v(" "),s("searchform",{on:{search:t.search}}),t._v(" "),t._l(t.messages,(function(t){return s("one-content",{key:t.id,attrs:{message:t}})})),t._v(" "),s("infinite-loading",{attrs:{spinner:"circles",identifier:t.searchData},on:{infinite:t.infiniteLoad}},[s("div",{staticClass:"text-center alert alert-secondary my-2 p-2",attrs:{slot:"no-more"},slot:"no-more"},[t._v("\n      メーリスは以上です\n    ")]),t._v(" "),s("div",{staticClass:"text-center alert alert-secondary my-2 p-2",attrs:{slot:"no-results"},slot:"no-results"},[t._v("\n       表示できるメーリスはありませんでした\n    ")])]),t._v(" "),t._m(0)],2)};a._withStripped=!0;var n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("section",{staticClass:"content row border-bottom",attrs:{id:"message-id-"+String(t.message.id)}},[s("h4",{staticClass:"col-12 my-1"},[s("router-link",{attrs:{to:t.link}},[t._v(t._s(t.message.title))])],1),t._v(" "),s("div",{staticClass:"col-12"},[s("span",{staticClass:"float-left date small p-1"},[t._v(t._s(t.message.created_at))]),t._v(" "),s("span",{staticClass:"float-left ml-4 whosent"},[t._v(t._s(t.message.writer))]),t._v(" "),s("bookmark-star",{attrs:{id:Number(t.message.id),is_bookmarked:t.message.is_bookmarked}})],1),t._v(" "),s("article",{staticClass:"col-12 my-2"},[t._v("\n    "+t._s(t._f("trim")(t.message.content))+"\n  ")])])};n._withStripped=!0;var i=s(177),r={props:{message:{type:Object,required:!0}},components:{bookmarkStar:i.a},filters:{trim(t){let e=t.indexOf("\n");return e<0&&(e=0),t.slice(e,e+200)}},computed:{link(){return"./content/"+String(this.message.id)+"/"}}},o=(s(178),s(7)),l=Object(o.a)(r,n,[],!1,null,"2af44e69",null);l.options.__file="front/components/board/index-one-content.vue";var c=l.exports,d=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("form",{staticClass:"content row pb-3 border-bottom",on:{submit:t.submit}},[s("div",{staticClass:"col-12"},[s("div",{staticClass:"d-inline-block"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.is_kaisei,expression:"is_kaisei"}],staticClass:"d-none",attrs:{type:"checkbox",name:"is_kaisei",id:"is_kaisei"},domProps:{checked:Array.isArray(t.is_kaisei)?t._i(t.is_kaisei,null)>-1:t.is_kaisei},on:{change:[function(e){var s=t.is_kaisei,a=e.target,n=!!a.checked;if(Array.isArray(s)){var i=t._i(s,null);a.checked?i<0&&(t.is_kaisei=s.concat([null])):i>-1&&(t.is_kaisei=s.slice(0,i).concat(s.slice(i+1)))}else t.is_kaisei=n},t.toggleChanged]}}),t._v(" "),s("label",{attrs:{for:"is_kaisei"}},[t._v("回生メーリスのみ:")])]),t._v(" "),s("div",{staticClass:"d-inline-block"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.is_zenkai,expression:"is_zenkai"}],staticClass:"d-none",attrs:{type:"checkbox",name:"is_zenkai",id:"is_zenkai"},domProps:{checked:Array.isArray(t.is_zenkai)?t._i(t.is_zenkai,null)>-1:t.is_zenkai},on:{change:[function(e){var s=t.is_zenkai,a=e.target,n=!!a.checked;if(Array.isArray(s)){var i=t._i(s,null);a.checked?i<0&&(t.is_zenkai=s.concat([null])):i>-1&&(t.is_zenkai=s.slice(0,i).concat(s.slice(i+1)))}else t.is_zenkai=n},t.toggleChanged]}}),t._v(" "),s("label",{attrs:{for:"is_zenkai"}},[t._v("全回メーリスのみ:")])]),t._v(" "),s("div",{staticClass:"d-inline-block"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.is_bookmark,expression:"is_bookmark"}],staticClass:"d-none",attrs:{type:"checkbox",name:"is_bookmark",id:"is_bookmark"},domProps:{checked:Array.isArray(t.is_bookmark)?t._i(t.is_bookmark,null)>-1:t.is_bookmark},on:{change:[function(e){var s=t.is_bookmark,a=e.target,n=!!a.checked;if(Array.isArray(s)){var i=t._i(s,null);a.checked?i<0&&(t.is_bookmark=s.concat([null])):i>-1&&(t.is_bookmark=s.slice(0,i).concat(s.slice(i+1)))}else t.is_bookmark=n},t.toggleChanged]}}),t._v(" "),s("label",{attrs:{for:"is_bookmark"}},[t._v("ブックマークのみ:")])])]),t._v(" "),t.showButton?s("div",{staticClass:"col-12 my-2"},[s("input",{staticClass:"submit btn btn-warning btn-sm ml-2",attrs:{type:"submit",value:"絞り込み"}})]):t._e(),t._v(" "),s("div",{staticClass:"col-12"},[s("input",{directives:[{name:"model",rawName:"v-model",value:t.text,expression:"text"}],staticClass:"form-control formtext",attrs:{type:"text",name:"text",placeholder:"件名・本文で検索",id:"id_text"},domProps:{value:t.text},on:{input:function(e){e.target.composing||(t.text=e.target.value)}}}),t._v(" "),s("input",{staticClass:"submit btn btn-info btn-sm ml-2",attrs:{type:"submit",value:"検索"}})])])};d._withStripped=!0;var m={name:"searchform",data:()=>({is_kaisei:!1,is_zenkai:!1,is_bookmark:!1,text:"",showButton:!1}),methods:{toggleChanged(){this.showButton=!0},submit(t){t.preventDefault(),this.is_kaisei||this.is_kaisei||this.is_bookmark||(this.showButton=!1);const e={is_kaisei:this.is_kaisei,is_zenkai:this.is_zenkai,is_bookmark:this.is_bookmark,text:this.text};this.$emit("search",e)}}},p=(s(180),Object(o.a)(m,d,[],!1,null,"7e5bf265",null));p.options.__file="front/components/board/index-searchform.vue";var h={name:"index",components:{oneContent:c,searchform:p.exports},data:()=>({searchData:{}}),computed:{messages(){return this.$store.state.read.messages}},methods:{infiniteLoad(t){console.log(t),this.$store.dispatch("read/loadMessages",this.searchData).then(e=>{console.log(e),this.messages.length>0&&t.loaded(),!1===e.has_next&&t.complete()}).catch(e=>{console.log(e),t.error()})},search(t){this.$store.commit("read/clearMessages"),this.searchData=t}}},u=(s(182),Object(o.a)(h,a,[function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"sendlink"}},[e("a",{attrs:{href:"/send/"}},[e("span",[this._v("メーリスを送信する")]),this._v(" "),e("img",{attrs:{src:"/static/img/send.svg",height:"50",width:"50"}})])])}],!1,null,"24dfcdb8",null));u.options.__file="front/components/board/index.vue";e.default=u.exports},162:function(t,e,s){"use strict";s.r(e);var a=function(){var t=this,e=t.$createElement,s=t._self._c||e;return t.messageExists?s("div",[s("div",{staticClass:"message-title mb-2"},[s("router-back-arrow",{attrs:{href:"../../"}}),t._v(" "),s("h4",{staticClass:"d-inline-block m-0"},[t._v(t._s(t.message.title))])],1),t._v(" "),s("div",{staticClass:"col-sm-12 col-md-8 my-1 pl-0"},[s("span",{staticClass:"date d-inline-block"},[t._v(t._s(t.message.created_at))]),t._v(" "),s("span",{staticClass:"ml-4 whosent"},[t._v(t._s(t.message.writer))]),t._v(" "),s("bookmark-star",{attrs:{id:Number(t.message.id),is_bookmarked:t.message.is_bookmarked}})],1),t._v(" "),s("hr"),t._v(" "),s("div",{staticClass:"col-sm-12 col-md-8 content p-0",domProps:{innerHTML:t._s(t.message.html)}}),t._v(" "),t.attachments.length>0?[s("hr"),t._v(" "),s("div",{staticClass:"col-sm-12 col-md-8 my-1 pl-0"},[s("h6",[t._v("添付ファイル")]),t._v(" "),t._l(t.attachments,(function(e){return[e.is_image?s("img",{key:e.pk,staticStyle:{width:"100%","max-width":"560px"},attrs:{src:e.path}}):s("a",{key:e.pk,attrs:{href:"./attachment/"+e.pk+"/"}},[t._v("\n        "+t._s(e.filename)+"\n      ")])]}))],2)]:t._e(),t._v(" "),t.message.writer!=t.message.sender?[s("hr"),t._v(" "),s("p",{staticClass:"small"},[t._v("このメーリスは "+t._s(t.message.sender)+" によって代理送信されました。")])]:t._e(),t._v(" "),s("hr")],2):s("div",[t._v("\n  message does not exist\n")])};a._withStripped=!0;var n=s(177),i=s(184),r={props:{id:{type:Number,required:!0}},components:{bookmarkStar:n.a,routerBackArrow:i.default},data:()=>({messageExists:!1,message:{},attachments:[]}),created(){this.axios.get("/read/api/contentothers/"+String(this.id)+"/").then(t=>{console.log(t),this.attachments=t.data.attachments}).catch(t=>{console.log(t)});let t=this.$store.state.read.messages.find(t=>t.id==this.id);if(t)return this.messageExists=!0,void(this.message=t);console.log("直接アクセス"),this.axios.get("/read/api/content/"+String(this.id)+"/").then(t=>{console.log(t.data.message),this.messageExists=!0,this.message=t.data.message}).catch(t=>{console.log(t)})}},o=(s(187),s(7)),l=Object(o.a)(r,a,[],!1,null,"bcc59a6a",null);l.options.__file="front/components/board/content.vue";e.default=l.exports},163:function(t,e,s){var a=s(179);"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);(0,s(17).default)("2472e18e",a,!1,{})},164:function(t,e,s){var a=s(181);"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);(0,s(17).default)("6151ee26",a,!1,{})},165:function(t,e,s){var a=s(183);"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);(0,s(17).default)("1e17e33a",a,!1,{})},166:function(t,e,s){"use strict";var a=s(167),n=s.n(a);e.default=n.a},167:function(t,e){t.exports={name:"router-back-arrow",props:{href:{type:String,required:!1,default:"../"}},methods:{onclick(){this.$router.push(this.href)}}}},168:function(t,e,s){var a=s(186);"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);(0,s(17).default)("247fce90",a,!1,{})},169:function(t,e,s){var a=s(188);"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);(0,s(17).default)("2e76ae06",a,!1,{})},177:function(t,e,s){"use strict";var a=function(){var t=this.$createElement,e=this._self._c||t;return e("span",{staticClass:"float-right",on:{click:this.onclick}},[this.bookmarked?e("img",{attrs:{src:"/static/img/star_yl.png",width:"16",height:"16"}}):e("img",{attrs:{src:"/static/img/star_bk.png",width:"16",height:"16"}})])};a._withStripped=!0;var n={props:{id:{type:Number,required:!0},is_bookmarked:{type:Boolean,required:!1,default:!1}},data:()=>({bookmarked:!1}),created(){this.bookmarked=this.is_bookmarked},methods:{onclick(){this.axios.post("/read/api/bookmark/"+String(this.id)+"/",{data:"data"}).then(t=>{this.bookmarked="true"===t.data["updated-to"],this.$store.commit("read/updateBookmarked",{id:this.id,bool:"true"===t.data["updated-to"]})})}}},i=s(7),r=Object(i.a)(n,a,[],!1,null,null,null);r.options.__file="front/components/board/bookmark-star.vue";e.a=r.exports},178:function(t,e,s){"use strict";var a=s(163);s.n(a).a},179:function(t,e,s){(e=s(13)(!1)).push([t.i,"\n.content article[data-v-2af44e69]{\r\n  display: block;\r\n  white-space: nowrap;\r\n  text-overflow: ellipsis;\r\n  overflow: hidden;\n}\r\n",""]),t.exports=e},180:function(t,e,s){"use strict";var a=s(164);s.n(a).a},181:function(t,e,s){(e=s(13)(!1)).push([t.i,'\ninput.formtext[data-v-7e5bf265]{\r\n  display: inline-block;\r\n  width: calc(100% - 62px);\r\n  max-width: 400px;\n}\nlabel[data-v-7e5bf265]{\r\n    display: inline-block;\r\n    position: relative;\r\n    height: 1rem;\r\n    padding: 0.5rem 3rem 1rem 0;\r\n    margin: 0 0 0.5rem;\r\n    font-size: 0.7rem;\r\n    line-height: 0.7rem;\n}\nlabel[data-v-7e5bf265]:before{\r\n  display: inline-block;\r\n  content: "";\r\n  position: absolute;\r\n    right: 0.4rem;\r\n    top: 0.3rem;\r\n  width: 2.4rem;\r\n  height: 1.2rem;\r\n  margin: 0;\r\n  padding: 0;\r\n  border: 1px solid #999;\r\n  border-radius: 1rem;\r\n  transition: 0.2s;\n}\nlabel[data-v-7e5bf265]:after{\r\n  display: block;\r\n  content: "";\r\n  position: absolute;\r\n  top: 0.44rem;\r\n  right: 1.7rem;\r\n  width: 0.9rem;\r\n  height: 0.9rem;\r\n  border-radius: 0.75rem;\r\n  background-color: #999;\r\n  transition: 0.2s;\n}\ninput:checked + label[data-v-7e5bf265]:before{\r\n  border-color: #0ee08a;\n}\ninput:checked + label[data-v-7e5bf265]:after{\r\n  right: 0.62rem;\r\n  background-color: #0ee08a;\n}\r\n\r\n',""]),t.exports=e},182:function(t,e,s){"use strict";var a=s(165);s.n(a).a},183:function(t,e,s){(e=s(13)(!1)).push([t.i,"\ndiv#sendlink[data-v-24dfcdb8]{\r\n  position: fixed;\r\n  bottom: 3rem;\r\n  right: 8vw;\r\n  z-index: 10;\n}\ndiv#sendlink a[data-v-24dfcdb8]{\r\n  display: block;\r\n  position: relative;\r\n  height: 62px;\r\n  padding: 5px 16px;\r\n  border: 1px solid #3bc665;\r\n  border-radius: 33px;\r\n  text-decoration: none;\r\n  background-color: rgba(255,255,255,0.5);\r\n  transition: 0.4s;\r\n  overflow: hidden;\n}\ndiv#sendlink a span[data-v-24dfcdb8]{\r\n  display: none;\r\n  text-decoration: none;\r\n  color: #212529;\n}\ndiv#sendlink a.hover[data-v-24dfcdb8]{\r\n  border: 1px double #3bc665;\r\n  background-color: #ccf0d7;\n}\ndiv#sendlink a.hover span[data-v-24dfcdb8]{\r\n  display: inline;\n}\ndiv#sendlink a img[data-v-24dfcdb8]{\r\n  transform: scale(-1, 1);\r\n  margin: 0 -4px 0 0;\r\n  padding: 0 -3px;\n}\r\n",""]),t.exports=e},184:function(t,e,s){"use strict";var a=s(203),n=s(166),i=(s(185),s(7)),r=Object(i.a)(n.default,a.a,a.b,!1,null,"a8ed510e",null);r.options.__file="front/components/board/router-back-arrow.vue",e.default=r.exports},185:function(t,e,s){"use strict";var a=s(168);s.n(a).a},186:function(t,e,s){(e=s(13)(!1)).push([t.i,"\ndiv#back[data-v-a8ed510e]{\r\n  display: inline-block;\r\n  \r\n  height: 24px;\r\n  margin: 0 6px 0 0;\n}\n#back > span[data-v-a8ed510e]{\r\n  height: 24px;\r\n  width: 24px;\r\n  display: inline-block;\r\n  position: relative;\r\n  overflow: hidden;\r\n  margin: 0;\n}\n#back > span[data-v-a8ed510e]:before{\r\n  content: '';\r\n  height: 12px;\r\n  width: 12px;\r\n  display: block;\r\n  border: 1px solid #333;\r\n  border-right-width: 0;\r\n  border-bottom-width: 0;\r\n  transform: rotate(-45deg);\r\n  position: absolute;\r\n  top: 5px;\r\n  left: 5px;\n}\n#back > span[data-v-a8ed510e]:after{\r\n  content: '';\r\n  height: 1px;\r\n  width: 20px;\r\n  display: block;\r\n  background: #333;\r\n  position: absolute;\r\n  top: 10.5px;\r\n  left: 3px;\n}\r\n",""]),t.exports=e},187:function(t,e,s){"use strict";var a=s(169);s.n(a).a},188:function(t,e,s){(e=s(13)(!1)).push([t.i,"\n.message-title > *[data-v-bcc59a6a]{\r\n  vertical-align: bottom;\n}\np.content[data-v-bcc59a6a]{\r\n  white-space: pre-line;\n}\r\n",""]),t.exports=e},203:function(t,e,s){"use strict";s.d(e,"a",(function(){return a})),s.d(e,"b",(function(){return n}));var a=function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"back"}},[e("span",{on:{click:this.onclick}})])},n=[];a._withStripped=!0}}]);