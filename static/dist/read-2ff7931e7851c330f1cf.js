(window.webpackJsonp=window.webpackJsonp||[]).push([[6],{115:function(t,e,s){"use strict";s.r(e);var a=function(){var t=this,e=t.$createElement,s=t._self._c||e;return t.status.messageLoaded&&t.status.canRead?s("div",[s("div",{staticClass:"message-title mb-2"},[s("router-back-arrow",{attrs:{href:"../../"}}),t._v(" "),s("h4",{staticClass:"d-inline-block m-0"},[t._v(t._s(t.message.title))])],1),t._v(" "),s("div",{staticClass:"col-sm-12 col-md-8 my-1 pl-0"},[s("span",{staticClass:"date d-inline-block"},[t._v(t._s(t.message.created_at))]),t._v(" "),s("span",{staticClass:"ml-4 whosent"},[t._v(t._s(t.message.writer))]),t._v(" "),s("bookmark-star",{attrs:{id:Number(t.message.id),is_bookmarked:t.message.is_bookmarked}})],1),t._v(" "),s("hr"),t._v(" "),s("div",{staticClass:"col-sm-12 col-md-8 content p-0",domProps:{innerHTML:t._s(t.message.html)}}),t._v(" "),t.attachments.length>0?[s("hr"),t._v(" "),s("div",{staticClass:"col-sm-12 col-md-8 my-1 pl-0"},[s("h6",[t._v("添付ファイル")]),t._v(" "),t._l(t.attachments,(function(e){return[e.is_image?s("img",{key:e.pk,staticStyle:{width:"100%","max-width":"560px"},attrs:{src:e.path}}):s("a",{key:e.pk,attrs:{href:"/api/board/download/"+t.id+"/"+e.pk+"/"}},[t._v("\n        "+t._s(e.filename)+"\n      ")])]}))],2)]:t._e(),t._v(" "),t.message.writer!=t.message.sender?[s("hr"),t._v(" "),s("p",{staticClass:"small"},[t._v("このメーリスは "+t._s(t.message.sender)+" によって代理送信されました。")])]:t._e(),t._v(" "),s("hr")],2):t.status.messageLoaded?t.status.canRead?s("div",[t._v("\n  some error occured\n")]):s("div",[t._v("\n  You can not read this message or message does not exist.\n")]):s("div",[t._v("\n  Now loading...\n")])};a._withStripped=!0;var n=s(164),r=s(171),i={props:{id:{type:Number,required:!0}},components:{bookmarkStar:n.a,routerBackArrow:r.default},metaInfo(){return{title:this.message.title}},data:()=>({status:{messageLoaded:!1,canRead:!1},message:{},attachments:[]}),created(){this.axios.get("/api/board/contentothers/"+String(this.id)+"/").then(t=>{console.log(t),this.attachments=t.data.attachments}).catch(t=>{console.log(t)});let t=this.$store.state.read.messages.find(t=>t.id==this.id);if(t)return this.$set(this.status,"messageLoaded",!0),this.$set(this.status,"canRead",!0),void(this.message=t);console.log("直接アクセス"),this.axios.get("/api/board/content/"+String(this.id)+"/").then(t=>{this.message=t.data.message,this.$set(this.status,"messageLoaded",!0),this.$set(this.status,"canRead",!0)}).catch(t=>{console.log(t),this.$set(this.status,"messageLoaded",!0),this.$set(this.status,"canRead",!1)})}},o=(s(174),s(32)),d=Object(o.a)(i,a,[],!1,null,"bcc59a6a",null);d.options.__file="front/components/board/content.vue";e.default=d.exports},132:function(t,e,s){"use strict";var a=s(133),n=s.n(a);e.default=n.a},133:function(t,e){t.exports={name:"router-back-arrow",props:{href:{type:String,required:!1,default:"../"}},methods:{onclick(){if(this.sendboxMode)return this.$router.push("/mypage/sendbox/");this.$router.push(this.href)}},computed:{sendboxMode(){return this.$store.state.read.sendboxMode}}}},134:function(t,e,s){var a=s(173);"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);(0,s(48).default)("247fce90",a,!1,{})},135:function(t,e,s){var a=s(175);"string"==typeof a&&(a=[[t.i,a,""]]),a.locals&&(t.exports=a.locals);(0,s(48).default)("2e76ae06",a,!1,{})},171:function(t,e,s){"use strict";var a=s(227),n=s(132),r=(s(172),s(32)),i=Object(r.a)(n.default,a.a,a.b,!1,null,"a8ed510e",null);i.options.__file="front/components/board/router-back-arrow.vue",e.default=i.exports},172:function(t,e,s){"use strict";var a=s(134);s.n(a).a},173:function(t,e,s){(e=s(47)(!1)).push([t.i,"\ndiv#back[data-v-a8ed510e]{\r\n  display: inline-block;\r\n  \r\n  height: 24px;\r\n  margin: 0 6px 0 0;\n}\n#back > span[data-v-a8ed510e]{\r\n  height: 24px;\r\n  width: 24px;\r\n  display: inline-block;\r\n  position: relative;\r\n  overflow: hidden;\r\n  margin: 0;\n}\n#back > span[data-v-a8ed510e]:before{\r\n  content: '';\r\n  height: 12px;\r\n  width: 12px;\r\n  display: block;\r\n  border: 1px solid #333;\r\n  border-right-width: 0;\r\n  border-bottom-width: 0;\r\n  transform: rotate(-45deg);\r\n  position: absolute;\r\n  top: 5px;\r\n  left: 5px;\n}\n#back > span[data-v-a8ed510e]:after{\r\n  content: '';\r\n  height: 1px;\r\n  width: 20px;\r\n  display: block;\r\n  background: #333;\r\n  position: absolute;\r\n  top: 10.5px;\r\n  left: 3px;\n}\r\n",""]),t.exports=e},174:function(t,e,s){"use strict";var a=s(135);s.n(a).a},175:function(t,e,s){(e=s(47)(!1)).push([t.i,"\n.message-title > *[data-v-bcc59a6a]{\r\n  vertical-align: bottom;\n}\np.content[data-v-bcc59a6a]{\r\n  white-space: pre-line;\n}\r\n",""]),t.exports=e},227:function(t,e,s){"use strict";s.d(e,"a",(function(){return a})),s.d(e,"b",(function(){return n}));var a=function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"back"}},[e("span",{on:{click:this.onclick}})])},n=[];a._withStripped=!0}}]);