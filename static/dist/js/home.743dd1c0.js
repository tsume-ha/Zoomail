"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[177],{8770:function(e,n,s){s.r(n),s.d(n,{default:function(){return U}});var t=s(6252),a=s(3577),u=s(2001);const l=e=>((0,t.dD)("data-v-144edc1e"),e=e(),(0,t.Cn)(),e),r={class:"cancel-parent-container"},c=l((()=>(0,t._)("div",{class:"logo-wraper"},[(0,t._)("img",{id:"logo",class:"pure-img",src:u})],-1))),o=l((()=>(0,t._)("p",null,[(0,t._)("span",null,"京都大学を中心に活動する"),(0,t._)("span",null,"アコースティック軽音サークル"),(0,t._)("br"),(0,t._)("span",null,[(0,t.Uk)("「"),(0,t._)("a",{href:"https://ku-unplugged.net",target:"_blank"},"京大アンプラグド"),(0,t.Uk)("」")]),(0,t._)("span",null,"の部内連絡管理アプリ")],-1))),i={id:"top-info",class:"container"},p={class:"pure-g"},m={class:"pure-menu-custom pure-u-1 pure-u-md-1-2"},d=l((()=>(0,t._)("h4",{class:"pure-menu-heading"},"New Contents",-1))),g={class:"pure-menu-list"},_={class:"pure-menu-custom pure-u-1 pure-u-md-1-2"},w=l((()=>(0,t._)("h4",{class:"pure-menu-heading"},"Announcements",-1))),k={class:"pure-menu-list"},f={class:"announcement-content"},h={class:"small"};function v(e,n,s,u,l,v){const C=(0,t.up)("router-link");return(0,t.wg)(),(0,t.iD)("article",r,[c,o,(0,t._)("div",i,[(0,t._)("div",p,[(0,t._)("section",m,[d,(0,t._)("ul",g,[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)(u.newContents,(e=>((0,t.wg)(),(0,t.iD)("li",{key:e.id,class:"pure-menu-item"},[(0,t.Wm)(C,{to:e.path,class:"pure-menu-link"},{default:(0,t.w5)((()=>[(0,t.Uk)(" 【"+(0,a.zw)(e.genre)+"】 "+(0,a.zw)(e.title),1)])),_:2},1032,["to"])])))),128))])]),(0,t._)("section",_,[w,(0,t._)("ul",k,[((0,t.wg)(!0),(0,t.iD)(t.HY,null,(0,t.Ko)(u.announcements,(e=>((0,t.wg)(),(0,t.iD)("li",{key:e.id,class:"pure-menu-item"},[(0,t._)("div",f,[(0,t._)("time",h,(0,a.zw)(e.date),1),(0,t.Uk)(" "+(0,a.zw)(e.text),1)])])))),128))])])])])])}var C=s(2262),x=s(8637),D=s(8042),b={setup(){const e=(0,x.oR)(),n=(0,C.iH)([]),s=(0,C.iH)([]);return(0,t.bv)((()=>{D.Z.get("/api/home/index/").then((e=>{n.value=e.data.newContents,s.value=e.data.announcements})).catch((n=>{e.commit("message/addMessage",{level:"error",message:`${String(n.response.status)} ${n.response.statusText}`,appname:"index/index"}),console.error(n.response)}))})),{newContents:n,announcements:s}}},z=s(3744);const H=(0,z.Z)(b,[["render",v],["__scopeId","data-v-144edc1e"]]);var U=H},2001:function(e,n,s){e.exports=s.p+"static/dist/img/zoomail.4c935cf7.png"}}]);
//# sourceMappingURL=home.743dd1c0.js.map