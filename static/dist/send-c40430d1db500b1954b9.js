(window.webpackJsonp=window.webpackJsonp||[]).push([[2],{159:function(e,t,n){"use strict";n.r(t);var a=function(){var e=this.$createElement,t=this._self._c||e;return 0==this.process?t("send-input",{on:{confirm:this.toConfirm}}):1==this.process?t("send-confirm",{on:{send:this.send,backToInput:this.backToInput}}):2==this.process?t("send-finish"):t("div",[this._v("error")])};a._withStripped=!0;var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("section",[n("h3",[e._v("メーリス送信")]),e._v(" "),n("form",{staticClass:"my-3"},[n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-title")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-from")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-to")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-content")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-attachment")],1)]),e._v(" "),n("button",{staticClass:"btn btn-info",on:{click:e.validate}},[e._v("確認画面へ")])])};r._withStripped=!0;var i=function(){var e=this.$createElement;return(this._self._c||e)("input",{staticClass:"form-control",attrs:{type:"text",name:"title",placeholder:"件名",required:"",id:"id_title"}})};i._withStripped=!0;var s={},l=n(8),o=Object(l.a)(s,i,[],!1,null,null,null);o.options.__file="front/components/board/send-input-title.vue";var c=o.exports,d=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"my-2"},[n("div",{staticClass:"v-select-label"},[e._v("\n   From: \n  ")]),e._v(" "),n("select",{directives:[{name:"model",rawName:"v-model",value:e.selectedYear,expression:"selectedYear"}],staticClass:"form-control",attrs:{name:"year_choice",id:"year_choice"},on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.selectedYear=t.target.multiple?n:n[0]}}},e._l(e.years,(function(t){return n("option",{key:t,domProps:{value:t}},[e._v("\n      "+e._s(t)+"\n    ")])})),0),e._v(" "),n("select",{directives:[{name:"model",rawName:"v-model",value:e.selectedMember,expression:"selectedMember"}],staticClass:"form-control",attrs:{name:"member_choice",id:"member_choice"},on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.selectedMember=t.target.multiple?n:n[0]}}},e._l(e.memberChoices,(function(t){return n("option",{key:t.id,domProps:{value:t.id}},[e._v("\n      "+e._s(t.name)+"\n    ")])})),0)])};d._withStripped=!0;var p={data:()=>({years:[2020,2019,2018,2017],selectedYear:2018,members:{2018:[{id:1,name:"あああああ"},{id:2,name:"い"},{id:3,name:"う"}]},selectedMember:null}),computed:{memberChoices(){return this.members[String(this.selectedYear)]}}},v=(n(183),Object(l.a)(p,d,[],!1,null,"6d3931f8",null));v.options.__file="front/components/board/send-input-from.vue";var u=v.exports,m=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"my-2"},[n("div",{staticClass:"v-select-label"},[e._v("\n   To: \n  ")]),e._v(" "),n("div",{staticClass:"v-select-wraper"},[n("v-select",{attrs:{options:e.years,label:"label",reduce:function(e){return e.year},multiple:""},model:{value:e.selected,callback:function(t){e.selected=t},expression:"selected"}})],1)])};m._withStripped=!0;var f={data:()=>({years:[{year:0,label:"全回メーリス"},{year:2020,label:"2020 26期"},{year:2019,label:"2019 25期 会長："},{year:2018,label:"2018 24期 会長："}],selected:null})},h=(n(185),Object(l.a)(f,m,[],!1,null,"b1b9d456",null));h.options.__file="front/components/board/send-input-to.vue";var _=h.exports,b=function(){var e=this.$createElement;return(this._self._c||e)("textarea",{staticClass:"form-control",attrs:{name:"content",cols:"40",rows:"10",placeholder:"本文を入力",required:""}})};b._withStripped=!0;var g={},w=Object(l.a)(g,b,[],!1,null,null,null);w.options.__file="front/components/board/send-input-content.vue";var y=w.exports,x=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"attachent-wrapper p-0 my-2"},[n("label",{staticClass:"my-0",class:{"attachment-opened":e.opened},attrs:{for:"attachment-input"},on:{dragenter:e.dragEnter,dragleave:e.dragLeave,dragover:function(e){e.preventDefault()},drop:function(t){return t.preventDefault(),e.dropFile(t)}}},[e.opened?n("span",[e._v("ここに添付するファイルをドロップ")]):n("span",[e._v("添付ファイルを選択、もしくはここにドラッグ＆ドロップ")]),e._v(" "),n("input",{ref:"attachments",attrs:{type:"file",multiple:"",id:"attachment-input"},on:{change:e.onFileChange}})]),e._v(" "),e.files.length>0?n("div",{staticClass:"small text-secondary mx-2"},[e._v("\n    クリックすると新しいタブでファイルを確認できます\n  ")]):e._e(),e._v(" "),n("div",{staticClass:"attachment-preview"},e._l(e.files,(function(t){return n("div",{key:t.name+t.size,staticClass:"attachment-preview-wrapper"},[n("attachment-preview",{attrs:{file:t}}),e._v(" "),n("div",{staticClass:"file-cansel",on:{click:function(n){return e.cansel(t)}}},[e._v("×")])],1)})),0),e._v(" "),e.files.length>0?n("div",[e._v("\n    "+e._s(e.files.length)+"件が選択されています\n  ")]):e._e()])};x._withStripped=!0;var C=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"preview-content-wrapper",on:{click:e.openFile}},[e.isImage?n("img",{attrs:{src:e.imageURL,alt:"iamge-preview"}}):"application/pdf"==e.file.type?n("img",{attrs:{src:"/static/img/board/pdf-icon.png",alt:"pdf-icon"}}):n("img",{attrs:{src:"/static/img/board/file-icon.png",alt:"file-icon"}}),e._v(" "),n("div",{staticClass:"preview-file-name"},[e._v(e._s(e.file.name))])])};C._withStripped=!0;var k={data:()=>({imageURL:"",objectURL:""}),props:{file:{required:!0,type:File}},computed:{isImage(){return this.file.type.startsWith("image/")}},methods:{readImage(){let e=new FileReader;e.onload=this.loadImage,e.readAsDataURL(this.file),this.objectURL=URL.createObjectURL(this.file)},loadImage(e){new Image;this.imageURL=e.target.result},openFile(){this.objectURL&&window.open(this.objectURL,"filePreview")}},mounted(){this.readImage()},beforeDestroy(){URL.revokeObjectURL(this.file)}},j=(n(187),Object(l.a)(k,C,[],!1,null,"d768f210",null));j.options.__file="front/components/board/send-input-attachment-preview.vue";var E={data:()=>({opened:!1,files:[]}),components:{attachmentPreview:j.exports},methods:{onFileChange(){let e=this.$refs.attachments.files;console.log(e);for(const t of e)this.files.push(t)},dragEnter(e){console.log("Enter Drop Area"),this.opened=!0},dragLeave(e){console.log("leave Drop Area"),this.opened=!1},dropFile(e){console.log("Drop File"),this.opened=!1,console.log(event.dataTransfer.files);for(const e of event.dataTransfer.files)this.files.push(e)},cansel(e){const t=this.files.indexOf(e);this.files.splice(t,1)}}},$=(n(189),Object(l.a)(E,x,[],!1,null,"029f6a7d",null));$.options.__file="front/components/board/send-input-attachment.vue";var I=$.exports,L=function(){var e=this.$createElement;return(this._self._c||e)("div",[this._v("send-send_at")])};L._withStripped=!0;var O={},S=Object(l.a)(O,L,[],!1,null,null,null);S.options.__file="front/components/board/send-input-sendat.vue";var R={components:{inputTitle:c,inputFrom:u,inputTo:_,inputContent:y,inputAttachment:I,inputSendAt:S.exports},methods:{validate(){this.$emit("confirm")}}},F=Object(l.a)(R,r,[],!1,null,null,null);F.options.__file="front/components/board/send-input.vue";var U=F.exports,T=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("section",[n("h3",[e._v("メーリス送信確認")]),e._v(" "),e._m(0),e._v(" "),e._m(1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[n("div",{staticClass:"p-1 label"},[e._v("本文：")]),e._v(" "),n("div",{staticClass:"p-1 border rounded display",staticStyle:{"white-space":"pre-wrap"},domProps:{textContent:e._s(e.content)}})]),e._v(" "),e._m(2),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-4 mx-0",attrs:{id:"send-button-wraper"}},[n("button",{staticClass:"btn btn-secondary",on:{click:e.backToInput}},[e._v("戻る")]),e._v(" "),n("button",{staticClass:"btn btn-info",on:{click:e.send}},[e._v("送信する")])])])};T._withStripped=!0;var A={methods:{backToInput(){this.$emit("backToInput")},send:()=>!1},data:()=>({content:"本文本文本文本文本文本文本文本文本文\n本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文\n\n本文本文  本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本\n文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文"})},D=(n(191),Object(l.a)(A,T,[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[t("div",{staticClass:"p-1 label"},[this._v("件名：")]),this._v(" "),t("div",{staticClass:"p-1 border rounded display"},[this._v("タイトル")])])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[t("div",{staticClass:"p-1 label"},[this._v("送信先：")]),this._v(" "),t("div",{staticClass:"p-1 border rounded display"},[this._v("24期（会長：だれだれ）, 25期（会長：だれだれ）")])])},function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[t("div",{staticClass:"p-1 label"},[this._v("添付ファイル：")]),this._v(" "),t("div",{staticClass:"p-1 border rounded display"},[this._v("2件添付")])])}],!1,null,"e40c1ace",null));D.options.__file="front/components/board/send-confirm.vue";var z=D.exports,P=function(){var e=this.$createElement;return(this._self._c||e)("div",[this._v("send-finish-and-complete")])};P._withStripped=!0;var Y=Object(l.a)({},P,[],!1,null,null,null);Y.options.__file="front/components/board/send-finish-and-complete.vue";var M={name:"send",components:{sendInput:U,sendConfirm:z,sendFinish:Y.exports},data:()=>({process:0}),methods:{toConfirm(){this.process=1},backToInput(){this.process=0},send(){this.process=2}}},q=Object(l.a)(M,a,[],!1,null,null,null);q.options.__file="front/components/board/send.vue";t.default=q.exports},168:function(e,t,n){var a=n(184);"string"==typeof a&&(a=[[e.i,a,""]]),a.locals&&(e.exports=a.locals);(0,n(17).default)("5059a411",a,!1,{})},169:function(e,t,n){var a=n(186);"string"==typeof a&&(a=[[e.i,a,""]]),a.locals&&(e.exports=a.locals);(0,n(17).default)("64655940",a,!1,{})},170:function(e,t,n){var a=n(188);"string"==typeof a&&(a=[[e.i,a,""]]),a.locals&&(e.exports=a.locals);(0,n(17).default)("06abd4fd",a,!1,{})},171:function(e,t,n){var a=n(190);"string"==typeof a&&(a=[[e.i,a,""]]),a.locals&&(e.exports=a.locals);(0,n(17).default)("510a5360",a,!1,{})},172:function(e,t,n){var a=n(192);"string"==typeof a&&(a=[[e.i,a,""]]),a.locals&&(e.exports=a.locals);(0,n(17).default)("1dcf3bdb",a,!1,{})},183:function(e,t,n){"use strict";var a=n(168);n.n(a).a},184:function(e,t,n){(t=n(13)(!1)).push([e.i,"\n.v-select-label[data-v-6d3931f8]{\r\n  display: inline-block;\r\n  width: 3rem;\n}\n#year_choice[data-v-6d3931f8]{\r\n  display: inline-block;\r\n  width: 5rem;\r\n  padding: 6px;\n}\n#member_choice[data-v-6d3931f8]{\r\n  display: inline-block;\r\n  width: calc(100% - 9rem);\r\n  min-width: 8rem;\r\n  max-width: 18rem;\n}\r\n",""]),e.exports=t},185:function(e,t,n){"use strict";var a=n(169);n.n(a).a},186:function(e,t,n){(t=n(13)(!1)).push([e.i,"\n.v-select-label[data-v-b1b9d456]{\r\n  display: inline-block;\r\n  width: 3rem;\n}\n.v-select-wraper[data-v-b1b9d456]{\r\n  display: inline-block;\r\n  width: calc(100% - 4rem);\n}\r\n",""]),e.exports=t},187:function(e,t,n){"use strict";var a=n(170);n.n(a).a},188:function(e,t,n){(t=n(13)(!1)).push([e.i,"\n.preview-content-wrapper[data-v-d768f210]{\r\n  border: 1px solid #aaa;\r\n  border-radius: 4px;\r\n  width: 140px;\r\n  max-height: 180px;\r\n  margin: 0.5rem;\r\n  padding: 0.5rem;\r\n  overflow: hidden;\r\n  z-index: 1;\n}\nimg[data-v-d768f210]{\r\n  margin: 0 auto;\r\n  height: 100px;\r\n  display: block;\n}\n.preview-file-name[data-v-d768f210]{\r\n  font-size: 10px;\n}\r\n",""]),e.exports=t},189:function(e,t,n){"use strict";var a=n(171);n.n(a).a},190:function(e,t,n){(t=n(13)(!1)).push([e.i,"\n.attachent-wrapper label *[data-v-029f6a7d]{\r\n  pointer-events: none;\n}\n.attachent-wrapper > label[data-v-029f6a7d]{\r\n  display: inline-block;\r\n  border: 1px dotted #d6eef5;\r\n  border-radius: 4px;\r\n  background-color: #f1f9fc;\r\n  padding: 0.5rem 1rem;\r\n  transition: .5s;\n}\n.attachent-wrapper > label.attachment-opened[data-v-029f6a7d]{\r\n  display: block;\r\n  width: 100%;\r\n  text-align: center;\r\n  padding: 4rem;\n}\n#attachment-input[data-v-029f6a7d]{\r\n  display: none;\n}\n.attachment-preview[data-v-029f6a7d]{\r\n  display: flex;\r\n  flex-wrap: wrap;\r\n  align-items: baseline;\n}\n.attachment-preview-wrapper[data-v-029f6a7d]{\r\n  position: relative;\n}\n.file-cansel[data-v-029f6a7d]{\r\n  position: absolute;\r\n  text-align: center;\r\n  top: 0;\r\n  right: 0;\r\n  border: 1px solid #aaa;\r\n  border-radius: 4px;\r\n  margin: 0.5rem;\r\n  width: 32px;\r\n  height: 32px;\r\n  line-height: 30px;\r\n  font-size: 20px;\r\n  background-color: rgba(255, 255, 255, 0.4);\r\n  transition: .2s;\r\n  z-index: 2;\n}\n.file-cansel[data-v-029f6a7d]:hover{\r\n  background-color: rgb(250, 75, 75);\n}\r\n\r\n",""]),e.exports=t},191:function(e,t,n){"use strict";var a=n(172);n.n(a).a},192:function(e,t,n){(t=n(13)(!1)).push([e.i,"\n.display-wraper[data-v-e40c1ace]{\r\n  display: flex;\n}\n.display-wraper .label[data-v-e40c1ace]{\r\n  flex-grow: 0;\r\n  flex-shrink: 0;\r\n  flex-basis: auto;\n}\n.display-wraper .display[data-v-e40c1ace]{\r\n  flex-grow: 2;\r\n  flex-shrink: 2;\r\n  flex-basis: auto;\n}\n#send-button-wraper[data-v-e40c1ace]{\r\n  display: flex;\r\n  justify-content: space-between;\n}\r\n",""]),e.exports=t}}]);