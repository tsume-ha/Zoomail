"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[954],{6669:function(e,t,s){s.r(t),s.d(t,{default:function(){return w}});var a=s(6252),n=s(2262),l=s(3577),r=s(8042),u=s(8637);const o=e=>((0,a.dD)("data-v-42df42a0"),e=e(),(0,a.Cn)(),e),c=o((()=>(0,a._)("h3",null,"その他資料",-1))),i={class:"pure-menu-custom card"},d={class:"pure-menu-list pure-g"},p=["href"],h={key:0,class:"small"};var g={setup(e){const t=(0,u.oR)(),s=(0,n.qj)([]);return r.Z.get("/api/others/").then((e=>{s.length=0,s.push(...e.data.contents)})).catch((e=>{console.error(e.response),t.commit("message/addMessage",{level:"warning",message:"その他資料のデータを取得できませんでした。",appname:"others/index"})})),(e,t)=>((0,a.wg)(),(0,a.iD)("article",null,[c,(0,a._)("section",i,[(0,a._)("ul",d,[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)((0,n.SU)(s),(e=>((0,a.wg)(),(0,a.iD)("li",{class:"pure-menu-item others-content pure-u-1",key:e.id},[(0,a._)("div",null,[(0,a._)("a",{href:`/download/others/${e.id}/`,target:"_blank"},(0,l.zw)(e.title),9,p)]),e.detail?((0,a.wg)(),(0,a.iD)("p",h,(0,l.zw)(e.detail),1)):(0,a.kq)("",!0)])))),128))])])]))}},f=s(3744);const m=(0,f.Z)(g,[["__scopeId","data-v-42df42a0"]]);var w=m}}]);
//# sourceMappingURL=others.b4402807.js.map