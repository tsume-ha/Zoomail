"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[954],{8626:function(e,t,s){s.r(t),s.d(t,{default:function(){return v}});var a=s(6252),n=s(2262),l=s(3577),r=s(5492),c=s(8042),u=s(8410);const o=e=>((0,a.dD)("data-v-44cc8153"),e=e(),(0,a.Cn)(),e),i=o((()=>(0,a._)("h3",null,"その他資料",-1))),d={class:"pure-menu-custom card"},m={class:"pure-menu-list pure-g"},p=["href"],h={class:"small"},g=["datetime"],w={key:0,class:"small"};var f={setup(e){const t=(0,u.oR)(),s=(0,n.qj)([]);c.Z.get("/api/others/").then((e=>{s.length=0,s.push(...e.data.contents)})).catch((e=>{console.error(e.response),t.commit("message/addMessage",{level:"warning",message:"その他資料のデータを取得できませんでした。",appname:"others/index"})}));const o=e=>(0,r.Z)(e).format("YYYY/MM/DD hh:mm");return(e,t)=>((0,a.wg)(),(0,a.iD)("article",null,[i,(0,a._)("section",d,[(0,a._)("ul",m,[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)((0,n.SU)(s),(e=>((0,a.wg)(),(0,a.iD)("li",{class:"pure-menu-item others-content pure-u-1",key:e.id},[(0,a._)("div",null,[(0,a._)("a",{href:`/download/others/${e.id}/`,target:"_blank"},[(0,a.Uk)((0,l.zw)(e.title)+" ",1),(0,a._)("span",h,"( "+(0,l.zw)(e.size)+" )",1)],8,p),(0,a._)("time",{datetime:e.updatedAt,class:"small"}," 更新: "+(0,l.zw)(o(e.updatedAt)),9,g)]),e.detail?((0,a.wg)(),(0,a.iD)("p",w,(0,l.zw)(e.detail),1)):(0,a.kq)("",!0)])))),128))])])]))}},_=s(3744);const k=(0,_.Z)(f,[["__scopeId","data-v-44cc8153"]]);var v=k}}]);
//# sourceMappingURL=others.c422147e.js.map