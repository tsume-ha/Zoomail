(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{109:function(e,t,i){"use strict";i.r(t);var s=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",[e.sendboxMode?i("h3",[e._v("送信ボックス")]):i("h3",[e._v("メーリス一覧")]),e._v(" "),i("searchform",{on:{search:e.search}}),e._v(" "),e._l(e.messages,(function(e){return i("one-content",{key:e.id,attrs:{message:e}})})),e._v(" "),i("infinite-loading",{attrs:{spinner:"circles",identifier:e.searchData},on:{infinite:e.infiniteLoad}},[i("div",{staticClass:"text-center alert alert-secondary my-2 p-2",attrs:{slot:"no-more"},slot:"no-more"},[e._v("\n      メーリスは以上です\n    ")]),e._v(" "),i("div",{staticClass:"text-center alert alert-secondary my-2 p-2",attrs:{slot:"no-results"},slot:"no-results"},[e._v("\n       表示できるメーリスはありませんでした\n    ")])]),e._v(" "),e.sendboxMode?e._e():i("div",{attrs:{id:"sendlink"}},[i("router-link",{attrs:{to:"../../send/"}},[i("span",[e._v("メーリスを送信する")]),e._v(" "),i("img",{attrs:{src:"/static/img/send.svg",height:"50",width:"50"}})])],1)],2)};s._withStripped=!0;var n=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("section",{staticClass:"content row border-bottom",attrs:{id:"message-id-"+String(e.message.id)}},[i("h4",{staticClass:"col-12 my-1"},[i("router-link",{attrs:{to:e.link}},[e._v(e._s(e.message.title))])],1),e._v(" "),i("div",{staticClass:"col-12"},[i("span",{staticClass:"float-left date small p-1"},[e._v(e._s(e.message.created_at))]),e._v(" "),i("span",{staticClass:"float-left ml-4 whosent"},[e._v(e._s(e.message.writer))]),e._v(" "),i("bookmark-star",{attrs:{id:Number(e.message.id),is_bookmarked:e.message.is_bookmarked}})],1),e._v(" "),i("article",{staticClass:"col-12 my-2"},[e._v("\n    "+e._s(e._f("trim")(e.message.content))+"\n  ")])])};n._withStripped=!0;var a=i(164),r={props:{message:{type:Object,required:!0}},components:{bookmarkStar:a.a},filters:{trim(e){let t=e.indexOf("\n");return t<0&&(t=0),e.slice(t,t+200)}},computed:{link(){return"/read/content/"+String(this.message.id)+"/"}}},o=(i(165),i(32)),l=Object(o.a)(r,n,[],!1,null,"2af44e69",null);l.options.__file="front/components/board/index-one-content.vue";var d=l.exports,c=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("form",{staticClass:"content row pb-3 border-bottom",on:{submit:e.submit}},[i("div",{staticClass:"col-12"},[i("div",{staticClass:"d-inline-block"},[i("input",{directives:[{name:"model",rawName:"v-model",value:e.is_kaisei,expression:"is_kaisei"}],staticClass:"d-none",attrs:{type:"checkbox",name:"is_kaisei",id:"is_kaisei"},domProps:{checked:Array.isArray(e.is_kaisei)?e._i(e.is_kaisei,null)>-1:e.is_kaisei},on:{change:[function(t){var i=e.is_kaisei,s=t.target,n=!!s.checked;if(Array.isArray(i)){var a=e._i(i,null);s.checked?a<0&&(e.is_kaisei=i.concat([null])):a>-1&&(e.is_kaisei=i.slice(0,a).concat(i.slice(a+1)))}else e.is_kaisei=n},e.toggleChanged]}}),e._v(" "),i("label",{attrs:{for:"is_kaisei"}},[e._v("回生メーリスのみ:")])]),e._v(" "),i("div",{staticClass:"d-inline-block"},[i("input",{directives:[{name:"model",rawName:"v-model",value:e.is_zenkai,expression:"is_zenkai"}],staticClass:"d-none",attrs:{type:"checkbox",name:"is_zenkai",id:"is_zenkai"},domProps:{checked:Array.isArray(e.is_zenkai)?e._i(e.is_zenkai,null)>-1:e.is_zenkai},on:{change:[function(t){var i=e.is_zenkai,s=t.target,n=!!s.checked;if(Array.isArray(i)){var a=e._i(i,null);s.checked?a<0&&(e.is_zenkai=i.concat([null])):a>-1&&(e.is_zenkai=i.slice(0,a).concat(i.slice(a+1)))}else e.is_zenkai=n},e.toggleChanged]}}),e._v(" "),i("label",{attrs:{for:"is_zenkai"}},[e._v("全回メーリスのみ:")])]),e._v(" "),i("div",{staticClass:"d-inline-block"},[i("input",{directives:[{name:"model",rawName:"v-model",value:e.is_bookmark,expression:"is_bookmark"}],staticClass:"d-none",attrs:{type:"checkbox",name:"is_bookmark",id:"is_bookmark"},domProps:{checked:Array.isArray(e.is_bookmark)?e._i(e.is_bookmark,null)>-1:e.is_bookmark},on:{change:[function(t){var i=e.is_bookmark,s=t.target,n=!!s.checked;if(Array.isArray(i)){var a=e._i(i,null);s.checked?a<0&&(e.is_bookmark=i.concat([null])):a>-1&&(e.is_bookmark=i.slice(0,a).concat(i.slice(a+1)))}else e.is_bookmark=n},e.toggleChanged]}}),e._v(" "),i("label",{attrs:{for:"is_bookmark"}},[e._v("ブックマークのみ:")])])]),e._v(" "),e.showButton?i("div",{staticClass:"col-12 my-2"},[i("input",{staticClass:"submit btn btn-warning btn-sm ml-2",attrs:{type:"submit",value:"絞り込み"}})]):e._e(),e._v(" "),i("div",{staticClass:"col-12"},[i("input",{directives:[{name:"model",rawName:"v-model",value:e.text,expression:"text"}],staticClass:"form-control formtext",attrs:{type:"text",name:"text",placeholder:"件名・本文で検索",id:"id_text"},domProps:{value:e.text},on:{input:function(t){t.target.composing||(e.text=t.target.value)}}}),e._v(" "),i("input",{staticClass:"submit btn btn-info btn-sm ml-2",attrs:{type:"submit",value:"検索"}})])])};c._withStripped=!0;var m={name:"searchform",data:()=>({is_kaisei:!1,is_zenkai:!1,is_bookmark:!1,text:"",showButton:!1}),methods:{toggleChanged(){this.showButton=!0},submit(e){e.preventDefault(),this.is_kaisei||this.is_kaisei||this.is_bookmark||(this.showButton=!1);const t={is_kaisei:this.is_kaisei,is_zenkai:this.is_zenkai,is_bookmark:this.is_bookmark,text:this.text};this.$emit("search",t)}}},k=(i(167),Object(o.a)(m,c,[],!1,null,"7e5bf265",null));k.options.__file="front/components/board/index-searchform.vue";var p=k.exports,h={name:"index",metaInfo:{title:"メーリス一覧"},props:{sendboxMode:{required:!1,default:!1,type:Boolean}},mounted(){this.$store.commit("read/setSendboxMode",this.sendboxMode)},components:{oneContent:d,searchform:p},data:()=>({searchData:{}}),computed:{messages(){return this.$store.state.read.messages}},methods:{infiniteLoad(e){console.log(e),this.$store.dispatch("read/loadMessages",this.searchData).then(t=>{console.log(t),this.messages.length>0&&e.loaded(),!1===t.has_next&&e.complete()}).catch(t=>{console.log(t),e.error()})},search(e){this.$store.commit("read/clearMessages"),this.searchData=e}}},u=(i(169),Object(o.a)(h,s,[],!1,null,"24dfcdb8",null));u.options.__file="front/components/board/index.vue";t.default=u.exports},129:function(e,t,i){var s=i(166);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,i(48).default)("2472e18e",s,!1,{})},130:function(e,t,i){var s=i(168);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,i(48).default)("6151ee26",s,!1,{})},131:function(e,t,i){var s=i(170);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,i(48).default)("1e17e33a",s,!1,{})},164:function(e,t,i){"use strict";var s=function(){var e=this.$createElement,t=this._self._c||e;return t("span",{staticClass:"float-right",on:{click:this.onclick}},[this.bookmarked?t("img",{attrs:{src:"/static/img/star_yl.png",width:"16",height:"16"}}):t("img",{attrs:{src:"/static/img/star_bk.png",width:"16",height:"16"}})])};s._withStripped=!0;var n={props:{id:{type:Number,required:!0},is_bookmarked:{type:Boolean,required:!1,default:!1}},data:()=>({bookmarked:!1}),created(){this.bookmarked=this.is_bookmarked},methods:{onclick(){this.axios.post("/api/board/bookmark/"+String(this.id)+"/",{data:"data"}).then(e=>{this.bookmarked="true"===e.data["updated-to"],this.$store.commit("read/updateBookmarked",{id:this.id,bool:"true"===e.data["updated-to"]})})}}},a=i(32),r=Object(a.a)(n,s,[],!1,null,null,null);r.options.__file="front/components/board/bookmark-star.vue";t.a=r.exports},165:function(e,t,i){"use strict";var s=i(129);i.n(s).a},166:function(e,t,i){(t=i(47)(!1)).push([e.i,"\n.content article[data-v-2af44e69]{\r\n  display: block;\r\n  white-space: nowrap;\r\n  text-overflow: ellipsis;\r\n  overflow: hidden;\n}\nsection h4 a[data-v-2af44e69]{\r\n\tcolor: #0058B3;\n}\nsection:hover h4 a[data-v-2af44e69]{\r\n\tcolor: #0058B3;\n}\r\n",""]),e.exports=t},167:function(e,t,i){"use strict";var s=i(130);i.n(s).a},168:function(e,t,i){(t=i(47)(!1)).push([e.i,'\ninput.formtext[data-v-7e5bf265]{\r\n  display: inline-block;\r\n  width: calc(100% - 62px);\r\n  max-width: 400px;\n}\nlabel[data-v-7e5bf265]{\r\n    display: inline-block;\r\n    position: relative;\r\n    height: 1rem;\r\n    padding: 0.5rem 3rem 1rem 0;\r\n    margin: 0 0 0.5rem;\r\n    font-size: 0.7rem;\r\n    line-height: 0.7rem;\n}\nlabel[data-v-7e5bf265]:before{\r\n  display: inline-block;\r\n  content: "";\r\n  position: absolute;\r\n    right: 0.4rem;\r\n    top: 0.3rem;\r\n  width: 2.4rem;\r\n  height: 1.2rem;\r\n  margin: 0;\r\n  padding: 0;\r\n  border: 1px solid #999;\r\n  border-radius: 1rem;\r\n  transition: 0.2s;\n}\nlabel[data-v-7e5bf265]:after{\r\n  display: block;\r\n  content: "";\r\n  position: absolute;\r\n  top: 0.44rem;\r\n  right: 1.7rem;\r\n  width: 0.9rem;\r\n  height: 0.9rem;\r\n  border-radius: 0.75rem;\r\n  background-color: #999;\r\n  transition: 0.2s;\n}\ninput:checked + label[data-v-7e5bf265]:before{\r\n  border-color: #0ee08a;\n}\ninput:checked + label[data-v-7e5bf265]:after{\r\n  right: 0.62rem;\r\n  background-color: #0ee08a;\n}\r\n\r\n',""]),e.exports=t},169:function(e,t,i){"use strict";var s=i(131);i.n(s).a},170:function(e,t,i){(t=i(47)(!1)).push([e.i,"\ndiv#sendlink[data-v-24dfcdb8]{\r\n  position: fixed;\r\n  bottom: 3rem;\r\n  right: 8vw;\r\n  z-index: 10;\n}\ndiv#sendlink a[data-v-24dfcdb8]{\r\n  display: block;\r\n  position: relative;\r\n  height: 62px;\r\n  padding: 5px 16px;\r\n  border: 1px solid #3bc665;\r\n  border-radius: 33px;\r\n  text-decoration: none;\r\n  background-color: rgba(255,255,255,0.5);\r\n  transition: 0.4s;\r\n  overflow: hidden;\n}\ndiv#sendlink a span[data-v-24dfcdb8]{\r\n  display: none;\r\n  text-decoration: none;\r\n  color: #212529;\n}\ndiv#sendlink a.hover[data-v-24dfcdb8]{\r\n  border: 1px double #3bc665;\r\n  background-color: #ccf0d7;\n}\ndiv#sendlink a.hover span[data-v-24dfcdb8]{\r\n  display: inline;\n}\ndiv#sendlink a img[data-v-24dfcdb8]{\r\n  transform: scale(-1, 1);\r\n  margin: 0 -4px 0 0;\r\n  padding: 0 -3px;\n}\r\n",""]),e.exports=t}}]);