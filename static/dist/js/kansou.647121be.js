"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[941],{8412:function(e,t,n){n.r(t),n.d(t,{default:function(){return k}});var r=n(6252),a=n(3577);const s=["href"],l=(0,r._)("br",null,null,-1);function o(e,t,n,o,u,i){return(0,r.wg)(),(0,r.iD)("main",null,[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)(o.yearsSet,(e=>((0,r.wg)(),(0,r.iD)("section",{key:e},[(0,r._)("h4",null,(0,a.zw)(e)+"年度",1),((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)(o.getItems(e),(e=>((0,r.wg)(),(0,r.iD)("p",{key:e.id},[(0,r._)("a",{href:e.url,target:"_blank"},(0,a.zw)(e.title),9,s),l,(0,r.Uk)(" "+(0,a.zw)(e.performedAt),1)])))),128))])))),128))])}var u=n(5492),i=n(2262),f=n(8042),c=n(5501),d={setup(){const e=(0,c.oR)(),t=(0,i.qj)([]);f.Z.get("/api/kansou/").then((e=>{t.length=0,t.push(...e.data.kansou)})).catch((t=>{console.error(t.response),e.commit("message/addMessage",{level:"warning",message:"感想用紙のデータを取得できませんでした。",appname:"kansou/index"})}));const n=(0,i.Fl)((()=>t.map((e=>{const t=(0,u.Z)(e.date);let n=0;return n=t.isBefore((0,u.Z)().set({year:t.year(),month:3,day:1}))?t.year()-1:t.year(),n})))),r=(0,i.Fl)((()=>n.value.filter(((e,t,n)=>n.indexOf(e)===t)).reverse())),a=e=>t.filter((t=>(0,u.Z)(t.date).isBetween((0,u.Z)(`${e}-04-01`),(0,u.Z)(`${e+1}-04-01`),void 0,"[)"))).reverse(),s=e=>(0,u.Z)(e).format("YYYY/MM/DD"),l=(0,i.Fl)((()=>e.state.user.is_staff));return{yearsSet:r,kansouStaff:l,getItems:a,displayDate:s}}},g=n(3744);const p=(0,g.Z)(d,[["render",o]]);var k=p}}]);
//# sourceMappingURL=kansou.647121be.js.map