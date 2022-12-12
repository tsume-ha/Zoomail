"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[957],{9388:function(e,a,t){t.d(a,{Gw:function(){return r},Li:function(){return l},a$:function(){return s},md:function(){return n}});var o=t(5492);const n=e=>(0,o.Z)(e).format("M/DD (dd)"),r=e=>{const a=(0,o.Z)(e).format("d");return"0"===a?"text-danger":"6"===a?"text-primary":""},l=e=>null===e?"例会教室は未登録":e,s=e=>{switch(e){case"終日使用不可":case"使用不可":return"text-danger";case null:return"text-muted";case"(20時まで音出し不可)":return"text-success";default:return""}}},7573:function(e,a,t){t.r(a),t.d(a,{default:function(){return I}});var o=t(6252),n=t(3577),r=t(2262),l=t(5492),s=t(8042),u=t(9146),d=t(9388);const i=e=>((0,o.dD)("data-v-0d609b74"),e=e(),(0,o.Cn)(),e),m=i((()=>(0,o._)("h3",null,"例会教室",-1))),c={id:"today-room",class:"card"},p=(0,o.Uk)(" 今日( "),v=(0,o.Uk)(" )の例会教室は、"),g=i((()=>(0,o._)("br",null,null,-1))),_={id:"today-room-name"},f=(0,o.Uk)(" 「 "),w=(0,o.Uk)(" 」 "),k=(0,o.Uk)(" です。 "),U={key:0,id:"register",class:"card"},h=i((()=>(0,o._)("h4",null,"教室係用メニュー",-1))),y=(0,o.Uk)("例会教室データの修正・登録 "),b={id:"ical",class:"card"},D=i((()=>(0,o._)("h4",null,"Googleカレンダー連携",-1))),S=i((()=>(0,o._)("p",null,[(0,o.Uk)(" Googleカレンダーなどに例会教室データを表示できるようにしました。"),(0,o._)("br"),(0,o.Uk)("くわしくは下のリンクから ")],-1))),C={href:"/howto/meeting_room/",class:"button button-primary",target:"_blank"},x=(0,o.Uk)("Googleカレンダー連携の方法 "),Z={id:"rooms",class:"card"},H=i((()=>(0,o._)("h4",null,"1カ月先までの例会教室一覧",-1))),z={key:0},G={key:1,class:"pure-table pure-table-bordered"};var M={__name:"index",setup(e){const a=(0,u.oR)(),t=(0,o.Fl)((()=>a.state.mypage.userInfo.canRegisterMeetingRoom)),i=(0,r.iH)([]);s.Z.get("/api/meeting_room/get31day/").then((e=>{i.value=e.data.rooms}));const M=(0,o.Fl)((()=>{const e=(0,l.Z)().format("YYYY-MM-DD"),a=i.value.find((a=>a.date===e));return void 0===a?{date:e,room:null}:a}));return(e,a)=>{const l=(0,o.up)("Icon"),s=(0,o.up)("router-link");return(0,o.wg)(),(0,o.iD)("article",null,[m,(0,o._)("div",c,[p,(0,o._)("span",{class:(0,n.C_)((0,r.SU)(d.Gw)((0,r.SU)(M).date))},(0,n.zw)((0,r.SU)(d.md)((0,r.SU)(M).date)),3),v,g,(0,o._)("span",_,[f,(0,o._)("span",{class:(0,n.C_)((0,r.SU)(d.a$)((0,r.SU)(M).room))},(0,n.zw)((0,r.SU)(d.Li)((0,r.SU)(M).room)),3),w]),k]),(0,r.SU)(t)?((0,o.wg)(),(0,o.iD)("div",U,[h,(0,o.Wm)(s,{to:{name:"meeting_room:register"},class:"button button-primary"},{default:(0,o.w5)((()=>[y,(0,o.Wm)(l,{icon:["fas","edit"]})])),_:1})])):(0,o.kq)("",!0),(0,o._)("div",b,[D,S,(0,o._)("a",C,[x,(0,o.Wm)(l,{icon:["far","calendar-plus"]})])]),(0,o._)("div",Z,[H,0===i.value.length?((0,o.wg)(),(0,o.iD)("p",z,"Now Loading...")):((0,o.wg)(),(0,o.iD)("table",G,[((0,o.wg)(!0),(0,o.iD)(o.HY,null,(0,o.Ko)(i.value,(e=>((0,o.wg)(),(0,o.iD)("tr",{key:e.date},[(0,o._)("td",null,[(0,o._)("span",{class:(0,n.C_)((0,r.SU)(d.Gw)(e.date))},(0,n.zw)((0,r.SU)(d.md)(e.date)),3)]),(0,o._)("td",null,[(0,o._)("span",{class:(0,n.C_)((0,r.SU)(d.a$)(e.room))},(0,n.zw)((0,r.SU)(d.Li)(e.room)),3)])])))),128))]))])])}}},R=t(3744);const Y=(0,R.Z)(M,[["__scopeId","data-v-0d609b74"]]);var I=Y},5293:function(e,a,t){t.r(a),t.d(a,{default:function(){return Z}});var o=t(6252),n=t(3577),r=t(2262),l=t(9963),s=t(2201),u=t(9146),d=t(8042),i=t(5492),m=t(9388);const c=e=>((0,o.dD)("data-v-0fe12a3d"),e=e(),(0,o.Cn)(),e),p=c((()=>(0,o._)("h3",null,"例会教室登録・修正",-1))),v={class:"card"},g={autocomplete:"off",class:"pure-menu pure-form"},_={class:"pure-menu-heading"},f={class:"pure-menu-list"},w={class:"date"},k={class:"room"},U=["onUpdate:modelValue","onChange"],h=(0,o.uE)('<datalist id="rooms-presets" data-v-0fe12a3d><option value="学生集会所 3階共用室" data-v-0fe12a3d></option><option value="学生集会所 2階共用室" data-v-0fe12a3d></option><option value="4共21" data-v-0fe12a3d></option><option value="4共22" data-v-0fe12a3d></option><option value="4共24" data-v-0fe12a3d></option><option value="4共30" data-v-0fe12a3d></option><option value="4共31" data-v-0fe12a3d></option></datalist>',1),y={class:"pure-control-group custom-two-buttons-wrapper"},b=(0,o.Uk)("戻る"),D={key:0,id:"api-saving-text"};var S={__name:"register",setup(e){const a=(0,u.oR)(),t=(0,s.tv)(),c=(0,o.Fl)((()=>a.state.mypage.userInfo.canRegisterMeetingRoom));c.value||(a.commit("message/addMessage",{level:"warning",message:"教室係の権限が無いようです",appname:"meeting_room/register"}),t.push({name:"meeting_room:index"}));const S=(0,i.Z)(),C=(0,r.iH)(S.year()),x=(0,r.iH)(S.month()+1),Z=(0,r.iH)([]),H=(0,r.iH)(!1),z=async(e,a)=>{H.value=!0;const t=await d.Z.get("/api/meeting_room/get_by_month/",{params:{year:e,month:a}});Z.value=t.data.rooms,H.value=!1};z(C.value,x.value);const G=(0,r.iH)(0),M=async e=>{const t=Z.value.find((a=>a.date===e)),o=new FormData;o.set("date",t.date),o.set("room_name",t.room||""),G.value++;const n=await d.Z.post("/api/meeting_room/register/",o);G.value--,n.data.room===t.room&&n.data.date===t.date||""===t.room&&null===n.data.room||(Z.value=[...[...Z.value].map((e=>e.date===t.date?{...n.data}:e))],a.commit("message/addMessage",{level:"warning",message:`${t.date}のデータが更新に失敗しました`,appname:"meeting_room/register"}))},R=async e=>{const a=(0,i.Z)([C.value,x.value-1]);a.add(e,"months"),C.value=a.year(),x.value=a.month()+1,Z.value.length=0,await z(C.value,x.value)};return(e,a)=>{const t=(0,o.up)("router-link");return(0,o.wg)(),(0,o.iD)("article",null,[p,(0,o._)("div",v,[(0,o._)("form",g,[(0,o._)("h4",_,(0,n.zw)(C.value)+"年"+(0,n.zw)(x.value)+"月",1),(0,o._)("ul",f,[((0,o.wg)(!0),(0,o.iD)(o.HY,null,(0,o.Ko)(Z.value,(e=>((0,o.wg)(),(0,o.iD)("li",{key:e.date,class:"pure-menu-item"},[(0,o._)("div",w,[(0,o._)("span",{class:(0,n.C_)((0,r.SU)(m.Gw)(e.date))},(0,n.zw)((0,r.SU)(m.md)(e.date)),3)]),(0,o._)("div",k,[(0,o.wy)((0,o._)("input",{type:"text","onUpdate:modelValue":a=>e.room=a,onChange:a=>M(e.date),placeholder:"未登録",list:"rooms-presets"},null,40,U),[[l.nr,e.room]])])])))),128)),h])]),(0,o._)("div",y,[(0,o._)("button",{onClick:a[0]||(a[0]=e=>R(-1)),class:"pure-button button-primary"}," 前の月 "),(0,o._)("button",{onClick:a[1]||(a[1]=e=>R(1)),class:"pure-button button-primary"}," 次の月 ")])]),(0,o.Wm)(t,{to:{name:"meeting_room:index"},class:"pure-button return"},{default:(0,o.w5)((()=>[b])),_:1}),G.value>0?((0,o.wg)(),(0,o.iD)("div",D,"saving...")):(0,o.kq)("",!0)])}}},C=t(3744);const x=(0,C.Z)(S,[["__scopeId","data-v-0fe12a3d"]]);var Z=x}}]);
//# sourceMappingURL=meeting_room.0c03f6d6.js.map