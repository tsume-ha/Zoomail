"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[954],{6426:function(e,t,n){n.r(t),n.d(t,{default:function(){return w}});var a=n(6252),s=n(3577),l=n(2262),r=n(8042),u=n(9146);const o=e=>((0,a.dD)("data-v-42df42a0"),e=e(),(0,a.Cn)(),e),c=o((()=>(0,a._)("h3",null,"その他資料",-1))),i={class:"pure-menu-custom card"},d={class:"pure-menu-list pure-g"},p=["href"],h={key:0,class:"small"};var g={__name:"index",setup(e){const t=(0,u.oR)(),n=(0,l.qj)([]);return r.Z.get("/api/others/").then((e=>{n.length=0,n.push(...e.data.contents)})).catch((e=>{console.error(e.response),t.commit("message/addMessage",{level:"warning",message:"その他資料のデータを取得できませんでした。",appname:"others/index"})})),(e,t)=>((0,a.wg)(),(0,a.iD)("article",null,[c,(0,a._)("section",i,[(0,a._)("ul",d,[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)(n,(e=>((0,a.wg)(),(0,a.iD)("li",{class:"pure-menu-item others-content pure-u-1",key:e.id},[(0,a._)("div",null,[(0,a._)("a",{href:`/download/others/${e.id}/`,target:"_blank"},(0,s.zw)(e.title),9,p)]),e.detail?((0,a.wg)(),(0,a.iD)("p",h,(0,s.zw)(e.detail),1)):(0,a.kq)("",!0)])))),128))])])]))}},m=n(3744);const f=(0,m.Z)(g,[["__scopeId","data-v-42df42a0"]]);var w=f}}]);
//# sourceMappingURL=others.a161a637.js.map