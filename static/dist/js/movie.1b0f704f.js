"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[929],{7958:function(e,t,n){n.r(t),n.d(t,{default:function(){return k}});n(7658);var r=n(6252),a=n(3577),s=n(5492),i=n(2262),u=n(8042),l=n(3907);const c=e=>((0,r.dD)("data-v-46738496"),e=e(),(0,r.Cn)(),e),o=c((()=>(0,r._)("h3",null,"ライブ動画",-1))),d={class:"pure-menu-heading pure-u-1"},p=["datetime"],m={key:0,class:"youtube pure-u-1"},g=["src"],h=["innerHTML"];var w={__name:"index",setup(e){const t=(0,l.oR)(),n=(0,i.qj)([]);u.Z.get("/api/movie/").then((e=>{n.length=0,n.push(...e.data.movies)})).catch((e=>{console.error(e.response),t.commit("message/addMessage",{level:"warning",message:"ライブ動画のデータを取得できませんでした。",appname:"movie/index"})}));const c=e=>(0,s.Z)(e).format("YYYY/MM/DD");return(e,t)=>((0,r.wg)(),(0,r.iD)("article",null,[o,((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)(n,(e=>((0,r.wg)(),(0,r.iD)("section",{key:e.id,class:"pure-menu-custom card pure-g"},[(0,r._)("h4",d,[(0,r.Uk)((0,a.zw)(e.title)+" ",1),(0,r._)("time",{datetime:e.heldAt},"("+(0,a.zw)(c(e.heldAt))+")",9,p)]),e.url?((0,r.wg)(),(0,r.iD)("div",m,[(0,r._)("iframe",{width:"560",height:"315",class:"youtube_content",src:e.url,frameborder:"0",allow:"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture",allowfullscreen:""},null,8,g)])):(0,r.kq)("",!0),e.description?((0,r.wg)(),(0,r.iD)("div",{key:1,class:"pure-u-1",innerHTML:e.description},null,8,h)):(0,r.kq)("",!0)])))),128))]))}},f=n(3744);const v=(0,f.Z)(w,[["__scopeId","data-v-46738496"]]);var k=v}}]);
//# sourceMappingURL=movie.1b0f704f.js.map