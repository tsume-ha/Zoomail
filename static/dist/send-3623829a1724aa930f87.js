(window.webpackJsonp=window.webpackJsonp||[]).push([[8],{109:function(e,t,n){"use strict";n.r(t);var s=function(){var e=this.$createElement,t=this._self._c||e;return 0==this.process?t("send-input",{on:{confirm:this.goToConfirm}}):1==this.process?t("send-confirm",{on:{send:this.send,backToInput:this.backToInput}}):2==this.process?t("send-finish"):t("div",[this._v("error")])};s._withStripped=!0;var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("section",[n("h3",[e._v("メーリス送信")]),e._v(" "),n("form",{staticClass:"my-3"},[n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-title")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-from")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-to")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-content")],1),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 p-0"},[n("input-attachment")],1)]),e._v(" "),n("button",{staticClass:"btn",class:{"btn-info":e.is_valid,"btn-secondary":!e.is_valid},on:{click:e.onclick}},[e._v("\n    確認画面へ\n  ")])])};a._withStripped=!0;var i=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("input",{directives:[{name:"model",rawName:"v-model",value:e.title,expression:"title"}],staticClass:"form-control",attrs:{type:"text",name:"title",placeholder:"件名",required:"",id:"id_title"},domProps:{value:e.title},on:{input:function(t){t.target.composing||(e.title=t.target.value)}}}),e._v(" "),e.is_valid.length>0&&e.isValidationDisplay?n("validation-error-messages",{attrs:{messages:e.is_valid}}):e._e()],1)};i._withStripped=!0;var r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("ul",e._l(e.messages,(function(t){return n("li",{key:t,staticClass:"text-danger small my-1",domProps:{textContent:e._s(t)}})})),0)};r._withStripped=!0;var o={name:"validation-error-messages",props:{messages:{required:!0,type:Array}}},l=(n(182),n(32)),c=Object(l.a)(o,r,[],!1,null,"02c4082b",null);c.options.__file="front/components/board/send-validation-error.vue";var d=c.exports,p={data:()=>({isTouched:!1}),components:{validationErrorMessages:d},computed:{title:{get(){return this.$store.state.send.title},set(e){this.isTouched=!0,this.$store.commit("send/titleInput",e)}},is_valid(){return this.$store.getters["send/validateTitle"]},isValidationDisplay(){return this.$store.state.send.validate_clicked||this.isTouched}}},m=Object(l.a)(p,i,[],!1,null,null,null);m.options.__file="front/components/board/send-input-title.vue";var v=m.exports,u=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{staticClass:"my-2"},[n("div",{staticClass:"v-select-label"},[e._v("\n   From: \n  ")]),e._v(" "),n("select",{directives:[{name:"model",rawName:"v-model",value:e.selectedYear,expression:"selectedYear"}],staticClass:"form-control",attrs:{name:"year_choice",id:"year_choice"},on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.selectedYear=t.target.multiple?n:n[0]}}},e._l(e.years,(function(t){return n("option",{key:t,domProps:{value:t}},[e._v("\n      "+e._s(t)+"\n    ")])})),0),e._v(" "),n("select",{directives:[{name:"model",rawName:"v-model",value:e.selectedMember,expression:"selectedMember"}],staticClass:"form-control",attrs:{name:"member_choice",id:"member_choice"},on:{change:function(t){var n=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){return"_value"in e?e._value:e.value}));e.selectedMember=t.target.multiple?n:n[0]}}},e._l(e.memberChoices,(function(t){return n("option",{key:t.id,domProps:{value:t.id}},[e._v("\n      "+e._s(t.name)+"\n    ")])})),0)]),e._v(" "),e.is_valid.length>0&&e.isValidationDisplay?n("validation-error-messages",{attrs:{messages:e.is_valid}}):e._e()],1)};u._withStripped=!0;var h={components:{validationErrorMessages:d},computed:{selectedMember:{get(){return this.$store.state.send.writer_id},set(e){this.$store.commit("send/fromInput",e)}},selectedYear:{get(){return this.$store.state.send.writer_year},set(e){this.$store.commit("send/setWriterYear",e)}},years(){return this.$store.state.send.writer_years},members(){return this.$store.state.send.writer_choices},memberChoices(){const e=this.members.find(e=>e.year===this.selectedYear);return e?e.list:[]},is_valid(){return this.$store.getters["send/validateWriter"]},isValidationDisplay(){return this.$store.state.send.validate_clicked}}},f=(n(184),Object(l.a)(h,u,[],!1,null,"6d3931f8",null));f.options.__file="front/components/board/send-input-from.vue";var _=f.exports,g=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("div",{staticClass:"my-2"},[n("div",{staticClass:"v-select-label"},[e._v("\n    To: \n    ")]),e._v(" "),n("div",{staticClass:"v-select-wraper"},[n("v-select",{attrs:{options:e.years,label:"label",reduce:function(e){return e.year},multiple:""},model:{value:e.selected,callback:function(t){e.selected=t},expression:"selected"}},[n("span",{attrs:{slot:"no-options"},on:{click:function(t){e.$refs.select.open=!1}},slot:"no-options"},[e._v("\n        情報を取得中です\n      ")])])],1)]),e._v(" "),e.is_valid.length>0&&e.isValidationDisplay?n("validation-error-messages",{attrs:{messages:e.is_valid}}):e._e()],1)};g._withStripped=!0;var b={components:{validationErrorMessages:d},data:()=>({isTouched:!1}),computed:{selected:{get(){return this.$store.state.send.to},set(e){this.isTouched=!0,this.$store.commit("send/toInput",e)}},years(){return this.$store.state.send.to_groups},is_valid(){return this.$store.getters["send/validateTo"]},isValidationDisplay(){return this.$store.state.send.validate_clicked||this.isTouched}}},y=(n(186),Object(l.a)(b,g,[],!1,null,"b1b9d456",null));y.options.__file="front/components/board/send-input-to.vue";var w=y.exports,x=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("textarea",{directives:[{name:"model",rawName:"v-model",value:e.content,expression:"content"}],staticClass:"form-control",attrs:{name:"content",cols:"40",rows:"10",placeholder:"本文を入力",required:""},domProps:{value:e.content},on:{input:function(t){t.target.composing||(e.content=t.target.value)}}}),e._v(" "),e.is_valid.length>0&&e.isValidationDisplay?n("validation-error-messages",{attrs:{messages:e.is_valid}}):e._e()],1)};x._withStripped=!0;var C={data:()=>({isTouched:!1}),components:{validationErrorMessages:d},computed:{content:{get(){return this.$store.state.send.content},set(e){this.isTouched=!0,this.$store.commit("send/contentInput",e)}},is_valid(){return this.$store.getters["send/validateContent"]},isValidationDisplay(){return this.$store.state.send.validate_clicked||this.isTouched}}},$=Object(l.a)(C,x,[],!1,null,null,null);$.options.__file="front/components/board/send-input-content.vue";var k=$.exports,T=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"attachent-wrapper p-0 my-2"},[n("label",{staticClass:"my-0",class:{"attachment-opened":e.opened},attrs:{for:"attachment-input"},on:{dragenter:e.dragEnter,dragleave:e.dragLeave,dragover:function(e){e.preventDefault()},drop:function(t){return t.preventDefault(),e.dropFile(t)}}},[e.opened?n("span",[e._v("ここに添付するファイルをドロップ")]):n("span",[e._v("添付ファイルを選択、もしくはここにドラッグ＆ドロップ")]),e._v(" "),n("input",{ref:"attachments",attrs:{type:"file",multiple:"",id:"attachment-input"},on:{change:e.onFileChange}})]),e._v(" "),e.files.length>0?n("div",{staticClass:"small text-secondary mx-2"},[e._v("\n    クリックすると新しいタブでファイルを確認できます\n  ")]):e._e(),e._v(" "),n("div",{staticClass:"attachment-preview"},e._l(e.files,(function(t){return n("div",{key:t.name+t.size,staticClass:"attachment-preview-wrapper"},[n("attachment-preview",{attrs:{file:t}}),e._v(" "),n("div",{staticClass:"file-cansel",on:{click:function(n){return e.cansel(t)}}},[e._v("×")])],1)})),0),e._v(" "),e.files.length>0?n("div",{staticClass:"mx-2"},[e._v("\n    "+e._s(e.files.length)+"件が選択されています\n  ")]):e._e(),e._v(" "),e.is_valid.length>0?n("validation-error-messages",{attrs:{messages:e.is_valid}}):e._e()],1)};T._withStripped=!0;var E=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"preview-content-wrapper",on:{click:e.openFile}},[e.isImage?n("img",{attrs:{src:e.imageURL,alt:"iamge-preview"}}):"application/pdf"==e.file.type?n("img",{attrs:{src:"/static/img/board/pdf-icon.png",alt:"pdf-icon"}}):n("img",{attrs:{src:"/static/img/board/file-icon.png",alt:"file-icon"}}),e._v(" "),n("div",{staticClass:"preview-file-name"},[e._v(e._s(e.file.name))])])};E._withStripped=!0;var I={data:()=>({imageURL:"",objectURL:""}),props:{file:{required:!0,type:File}},computed:{isImage(){return this.file.type.startsWith("image/")}},methods:{readImage(){let e=new FileReader;e.onload=this.loadImage,e.readAsDataURL(this.file),this.objectURL=URL.createObjectURL(this.file)},loadImage(e){new Image;this.imageURL=e.target.result},openFile(){this.objectURL&&window.open(this.objectURL,"filePreview")}},mounted(){this.readImage()},beforeDestroy(){URL.revokeObjectURL(this.file)}},j=(n(188),Object(l.a)(I,E,[],!1,null,"d768f210",null));j.options.__file="front/components/board/send-input-attachment-preview.vue";var F=j.exports,O={data:()=>({opened:!1,files:[]}),components:{attachmentPreview:F,validationErrorMessages:d},beforeMount(){const e=this.$store.state.send.attachments;for(let t=0;t<e.length;t++)this.$set(this.files,t,e[t])},methods:{onFileChange(){let e=this.$refs.attachments.files;for(const t of e)this.files.push(t);this.commit()},dragEnter(e){console.log("Enter Drop Area"),this.opened=!0},dragLeave(e){console.log("leave Drop Area"),this.opened=!1},dropFile(e){console.log("Drop File"),this.opened=!1,console.log(event.dataTransfer.files);for(const e of event.dataTransfer.files)this.files.push(e);this.commit()},cansel(e){const t=this.files.indexOf(e);this.files.splice(t,1),this.commit()},commit(){const e=this.files.reduce((e,t)=>(e.some(e=>e.size===t.size&&e.name===t.name)?console.log("重複あり"):e.push(t),e),[]);this.files=e,this.$store.commit("send/fileInput",this.files)}},computed:{is_valid(){return this.$store.getters["send/validateAttachments"]}}},D=(n(190),Object(l.a)(O,T,[],!1,null,"029f6a7d",null));D.options.__file="front/components/board/send-input-attachment.vue";var L=D.exports,M=function(){var e=this.$createElement;return(this._self._c||e)("div",[this._v("send-send_at")])};M._withStripped=!0;var R={},S=Object(l.a)(R,M,[],!1,null,null,null);S.options.__file="front/components/board/send-input-sendat.vue";var U={components:{inputTitle:v,inputFrom:_,inputTo:w,inputContent:k,inputAttachment:L,inputSendAt:S.exports},methods:{onclick(){if(!this.is_valid)return this.$store.commit("send/validate"),!1;this.$emit("confirm")}},computed:{is_valid(){return this.$store.getters["send/isAllValid"]}},created(){this.$store.dispatch("send/getToGroups"),this.$store.dispatch("send/getFROMs")}},A=Object(l.a)(U,a,[],!1,null,null,null);A.options.__file="front/components/board/send-input.vue";var P=A.exports,V=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("section",[n("h3",[e._v("メーリス送信確認")]),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[n("div",{staticClass:"p-1 label"},[e._v("件名：")]),e._v(" "),n("div",{staticClass:"p-1 border rounded display"},[e._v(e._s(e.title))])]),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[n("div",{staticClass:"p-1 label"},[e._v("送信先：")]),e._v(" "),n("div",{staticClass:"p-1 border rounded display"},e._l(e.to_selected,(function(t){return n("span",{key:t.label,staticClass:"badge badge-pill badge-light mx-2 border rounded"},[e._v(e._s(t.label))])})),0)]),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[n("div",{staticClass:"p-1 label"},[e._v("本文：")]),e._v(" "),n("div",{staticClass:"p-1 border rounded display",staticStyle:{"white-space":"pre-wrap"},domProps:{textContent:e._s(e.content)}})]),e._v(" "),e.attachments.length?n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper"},[n("div",{staticClass:"p-1 label"},[e._v("添付ファイル：")]),e._v(" "),n("div",{staticClass:"p-1 border rounded display attachment-wraper"},[e._l(e.attachments,(function(e){return n("attachment-preview",{key:e.name+e.size,attrs:{file:e}})})),e._v(" "),n("div",{staticClass:"mx-2"},[e._v(e._s(e.attachments.length)+"件添付")])],2)]):e._e(),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-4 mx-0",attrs:{id:"send-button-wraper"}},[n("button",{staticClass:"btn btn-secondary",on:{click:e.backToInput}},[e._v("戻る")]),e._v(" "),n("button",{staticClass:"btn btn-info",on:{click:e.send}},[e._v("送信する")])])])};V._withStripped=!0;var z={components:{attachmentPreview:F},methods:{backToInput(){this.$emit("backToInput")},send(){this.$emit("send")}},computed:{title(){return this.$store.state.send.title},content(){return this.$store.state.send.content},to(){return this.$store.state.send.to},to_groups(){return this.$store.state.send.to_groups},to_selected(){return this.to_groups.filter(e=>this.to.includes(e.year))},attachments(){return this.$store.state.send.attachments}}},Y=(n(192),Object(l.a)(z,V,[],!1,null,"e40c1ace",null));Y.options.__file="front/components/board/send-confirm.vue";var q=Y.exports,N=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("h3",[e._v("メーリス送信")]),e._v(" "),n("div",{staticClass:"col-sm-12 col-md-10 col-lg-8 my-5 py-5",attrs:{id:"process-wrapper"}},[e.complete?n("h4",[e._v("送信完了！")]):n("h4",[e._v("送信中")]),e._v(" "),n("transition",{attrs:{mode:"out-in"}},[e.progress<100?n("div",{key:"uploading"},[e._v("\n        サーバーにデータを転送中（"+e._s(e.progress)+"%）\n      ")]):e.complete?e.complete?n("div",{key:"complete"},[e._v("\n        メーリスが"+e._s(e.complete_num)+"件送信されました\n      ")]):e._e():n("div",{key:"processing",domProps:{innerHTML:e._s(e.processingMessage[e.messageFrag])}})])],1),e._v(" "),n("button",{staticClass:"btn",class:{"btn-info":e.complete,"btn-secondary":!e.complete},on:{click:e.onclick}},[e._v("\n    メーリス一覧に戻る\n  ")])])};N._withStripped=!0;var W={data:()=>({processingMessage:["サーバーからメーリスを送信中","サーバーからメーリスを送信中...<br>10秒程度かかることもます。この画面のまましばらくお待ちください。"],messageFrag:0}),computed:{progress(){return this.$store.state.send.progress},complete(){return this.$store.state.send.complete},complete_num(){return this.$store.state.send.complete_num}},methods:{onclick(){if(!this.complete)return!1;window.location.href="/read/"}},watch:{progress(e,t){e&&window.setTimeout(()=>{this.messageFrag=1},2e3)}}},J=(n(194),Object(l.a)(W,N,[],!1,null,"4411f142",null));J.options.__file="front/components/board/send-finish-and-complete.vue";var G={name:"send",metaInfo:{title:"メーリス送信"},components:{sendInput:P,sendConfirm:q,sendFinish:J.exports},data:()=>({process:0}),methods:{goToConfirm(){this.process=1},backToInput(){this.process=0},send(){this.process=2,this.$store.dispatch("send/send")}}},H=Object(l.a)(G,s,[],!1,null,null,null);H.options.__file="front/components/board/send.vue";t.default=H.exports},138:function(e,t,n){var s=n(183);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,n(48).default)("4cb06718",s,!1,{})},139:function(e,t,n){var s=n(185);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,n(48).default)("5059a411",s,!1,{})},140:function(e,t,n){var s=n(187);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,n(48).default)("64655940",s,!1,{})},141:function(e,t,n){var s=n(189);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,n(48).default)("06abd4fd",s,!1,{})},142:function(e,t,n){var s=n(191);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,n(48).default)("510a5360",s,!1,{})},143:function(e,t,n){var s=n(193);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,n(48).default)("1dcf3bdb",s,!1,{})},144:function(e,t,n){var s=n(195);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);(0,n(48).default)("7f4cbce0",s,!1,{})},182:function(e,t,n){"use strict";var s=n(138);n.n(s).a},183:function(e,t,n){(t=n(47)(!1)).push([e.i,"\nul[data-v-02c4082b]{\r\n  list-style: none;\r\n  margin: 5px 0 0 1rem;\r\n  padding: 0;\n}\r\n",""]),e.exports=t},184:function(e,t,n){"use strict";var s=n(139);n.n(s).a},185:function(e,t,n){(t=n(47)(!1)).push([e.i,"\n.v-select-label[data-v-6d3931f8]{\r\n  display: inline-block;\r\n  width: 3rem;\n}\n#year_choice[data-v-6d3931f8]{\r\n  display: inline-block;\r\n  width: 5rem;\r\n  padding: 6px;\n}\n#member_choice[data-v-6d3931f8]{\r\n  display: inline-block;\r\n  width: calc(100% - 9rem);\r\n  min-width: 8rem;\r\n  max-width: 18rem;\n}\r\n",""]),e.exports=t},186:function(e,t,n){"use strict";var s=n(140);n.n(s).a},187:function(e,t,n){(t=n(47)(!1)).push([e.i,"\n.v-select-label[data-v-b1b9d456]{\r\n  display: inline-block;\r\n  width: 3rem;\n}\n.v-select-wraper[data-v-b1b9d456]{\r\n  display: inline-block;\r\n  width: calc(100% - 4rem);\n}\r\n",""]),e.exports=t},188:function(e,t,n){"use strict";var s=n(141);n.n(s).a},189:function(e,t,n){(t=n(47)(!1)).push([e.i,"\n.preview-content-wrapper[data-v-d768f210]{\r\n  border: 1px solid #aaa;\r\n  border-radius: 4px;\r\n  width: 140px;\r\n  max-height: 180px;\r\n  margin: 0.5rem;\r\n  padding: 0.5rem;\r\n  overflow: hidden;\r\n  z-index: 1;\n}\nimg[data-v-d768f210]{\r\n  margin: 0 auto;\r\n  height: 100px;\r\n  display: block;\n}\n.preview-file-name[data-v-d768f210]{\r\n  font-size: 10px;\n}\r\n",""]),e.exports=t},190:function(e,t,n){"use strict";var s=n(142);n.n(s).a},191:function(e,t,n){(t=n(47)(!1)).push([e.i,"\n.attachent-wrapper label *[data-v-029f6a7d]{\r\n  pointer-events: none;\n}\n.attachent-wrapper > label[data-v-029f6a7d]{\r\n  display: inline-block;\r\n  border: 1px dotted #d6eef5;\r\n  border-radius: 4px;\r\n  background-color: #f1f9fc;\r\n  padding: 0.5rem 1rem;\r\n  transition: .5s;\n}\n.attachent-wrapper > label.attachment-opened[data-v-029f6a7d]{\r\n  display: block;\r\n  width: 100%;\r\n  text-align: center;\r\n  padding: 4rem;\n}\n#attachment-input[data-v-029f6a7d]{\r\n  display: none;\n}\n.attachment-preview[data-v-029f6a7d]{\r\n  display: flex;\r\n  flex-wrap: wrap;\r\n  align-items: baseline;\n}\n.attachment-preview-wrapper[data-v-029f6a7d]{\r\n  position: relative;\n}\n.file-cansel[data-v-029f6a7d]{\r\n  position: absolute;\r\n  text-align: center;\r\n  top: 0;\r\n  right: 0;\r\n  border: 1px solid #aaa;\r\n  border-radius: 4px;\r\n  margin: 0.5rem;\r\n  width: 32px;\r\n  height: 32px;\r\n  line-height: 30px;\r\n  font-size: 20px;\r\n  background-color: rgba(255, 255, 255, 0.4);\r\n  transition: .2s;\r\n  z-index: 2;\n}\n.file-cansel[data-v-029f6a7d]:hover{\r\n  background-color: rgba(255, 255, 255, 0.95);\n}\r\n\r\n",""]),e.exports=t},192:function(e,t,n){"use strict";var s=n(143);n.n(s).a},193:function(e,t,n){(t=n(47)(!1)).push([e.i,"\n.display-wraper[data-v-e40c1ace]{\r\n  display: flex;\n}\n.display-wraper .label[data-v-e40c1ace]{\r\n  flex-grow: 0;\r\n  flex-shrink: 0;\r\n  flex-basis: auto;\n}\n.display-wraper .display[data-v-e40c1ace]{\r\n  flex-grow: 2;\r\n  flex-shrink: 2;\r\n  flex-basis: auto;\n}\n#send-button-wraper[data-v-e40c1ace]{\r\n  display: flex;\r\n  justify-content: space-between;\n}\n.attachment-wraper[data-v-e40c1ace]{\r\n  display: flex;\r\n  flex-wrap: wrap;\r\n  align-items: baseline;\n}\r\n",""]),e.exports=t},194:function(e,t,n){"use strict";var s=n(144);n.n(s).a},195:function(e,t,n){(t=n(47)(!1)).push([e.i,"\n#process-wrapper[data-v-4411f142]{\r\n  border: 1px #eeeeee dotted;\r\n  text-align: center;\n}\n.v-enter-active[data-v-4411f142], .v-leave-active[data-v-4411f142]{\r\n  transition: margin,opacity .3s;\n}\n.v-enter[data-v-4411f142]{\r\n  margin-top: 10px;\r\n  margin-bottom: -10px;\r\n  opacity: 0;\n}\n.v-enter-to[data-v-4411f142], .v-leave[data-v-4411f142]{\r\n  margin-top: 0;\r\n  margin-bottom: 0;\r\n  opacity: 1;\n}\n.v-leave-to[data-v-4411f142]{\r\n  margin-top: -10px;\r\n  margin-bottom: 10px;\r\n  opacity: 0;\n}\r\n",""]),e.exports=t}}]);