<template>
  <header class="row content-header">
    <router-link :to="path" class="back-arrow"></router-link>
    <h3>{{text}}</h3>
  </header>
</template>

<script>
export default {
  props: {
    path: {type: String, required: false, default: "../"},
    text: {type: String, required: true}
  }
}
</script>

<style scoped>
.content-header{
  display: flex;
  margin: 0;
  padding: 0;
  height: 2rem;
  width: 100%;
  border-bottom: 1px solid #333;
}
.content-header h3{
  font-size: 1.5rem;

}
.back-arrow{
  height: 24px;
  width: 24px;
  display: block;
  position: relative;
  overflow: hidden;
  margin: 3px 0.5rem 3px 0.25rem;
}
.back-arrow:before{
  content: '';
  height: 12px;
  width: 12px;
  display: block;
  border: 1px solid #333;
  border-right-width: 0;
  border-bottom-width: 0;
  transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  position: absolute;
  top: 5px;
  left: 5px;
}
.back-arrow:after{
  content: '';
  height: 1px;
  width: 20px;
  display: block;
  background: #333;
  position: absolute;
  top: 10.5px;
  left: 3px;
}
</style>