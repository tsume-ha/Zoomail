"use strict";(self["webpackChunkfront"]=self["webpackChunkfront"]||[]).push([[17],{6771:function(e,t,a){a.r(t),a.d(t,{default:function(){return D}});var s=a(6252),r=a(3577),l=a(7688);const n=e=>((0,s.dD)("data-v-4d2c5b87"),e=e(),(0,s.Cn)(),e),o=n((()=>(0,s._)("h3",null,"写真",-1))),u=n((()=>(0,s._)("p",null,[(0,s.Uk)(" アンプラのイベントの写真を公開しています。"),(0,s._)("br"),(0,s.Uk)(" LiveLogに登録されていないBBQやお花見のイベントの写真もあります! ")],-1))),i={class:"pure-g"},p=["href"],c=["src","alt"],d=["alt"],h={class:"photo-title"},g={class:"photo-date"};function m(e,t,a,n,m,f){return(0,s.wg)(),(0,s.iD)("article",null,[o,u,(0,s._)("div",i,[((0,s.wg)(!0),(0,s.iD)(s.HY,null,(0,s.Ko)(n.photos,(e=>((0,s.wg)(),(0,s.iD)("div",{key:"photo-"+e.id,class:"pure-u-1-2 pure-u-sm-1-3 pure-u-md-1-4 pure-u-lg-1-5 card-wrapper"},[(0,s._)("a",{href:e.url,class:"card-photo",target:"_blank"},[e.thumbnail?((0,s.wg)(),(0,s.iD)("img",{key:0,src:e.thumbnail,alt:`${e.title} - サムネイル`,class:"pure-img"},null,8,c)):((0,s.wg)(),(0,s.iD)("img",{key:1,src:l,alt:`${e.title} - サムネイル`,class:"pure-img"},null,8,d)),(0,s._)("span",h,(0,r.zw)(e.title),1),(0,s._)("span",g,(0,r.zw)(n.displayDate(e.date)),1)],8,p)])))),128))])])}var f=a(5492),_=a(2262),v=a(8042),b=a(8410),w={setup(){const e=(0,b.oR)(),t=(0,_.qj)([]);v.Z.get("/api/photo/").then((e=>{t.length=0,t.push(...e.data.photos)})).catch((t=>{console.error(t.response),e.commit("message/addMessage",{level:"warning",message:"アルバムを取得できませんでした。",appname:"photos/index"})}));const a=(0,s.Fl)((()=>t.map((e=>{const t=(0,f.Z)(e.date);let a=0;return a=t.isBefore((0,f.Z)().set({year:t.year(),month:3,day:1}))?t.year()-1:t.year(),a})))),r=(0,s.Fl)((()=>a.value.filter(((e,t,a)=>a.indexOf(e)===t)).reverse())),l=e=>t.filter((t=>(0,f.Z)(t.date).isBetween((0,f.Z)(`${e}-04-01`),(0,f.Z)(`${e+1}-04-01`),void 0,"[)"))).reverse(),n=e=>(0,f.Z)(e).format("YYYY/MM/DD"),o=e=>e.thumbnail?e.thumbnail:"/static/img/album_thum_default.jpg",u=(0,s.Fl)((()=>e.state.user.is_staff));return{photos:t,years:a,yearsSet:r,photoStaff:u,getItems:l,displayDate:n,thumbnailPath:o}}},y=a(3744);const k=(0,y.Z)(w,[["render",m],["__scopeId","data-v-4d2c5b87"]]);var D=k},7688:function(e,t,a){e.exports=a.p+"img/unplugged_logo.c717fdac.jpg"}}]);
//# sourceMappingURL=photo.bc0ca7b2.js.map