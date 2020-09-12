<template>
  <div class="wrap">
    <div class="innner-wrap">
      <span class="rotate"> </span><br>
      <span class="text">{{text}}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'nowloading',
  props: {
    text: {required: false, type: String, default: ''},
  }
}
</script>

<style scoped>
div.wrap{
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  top: 0;
  left: 0;
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.7);
}
div.inner-wrap{
  position: relative;
  text-align: center;
  width: 200px;
}
span.rotate{
  width: 60px;
  height: 60px;
  display: inline-block;
  position: relative;
  border-top: 8px #31b1e4 solid;
  border-right: 8px #31b1e4 solid;
  border-bottom: 8px #31b1e4 solid;
  border-left: 8px transparent solid;
  border-radius: 50%;
  animation: 1s linear infinite rotation;
}
@keyframes rotation{
  0%{ transform:rotate(0);}
  100%{ transform:rotate(360deg); }
}
span.text{
  text-shadow: 0 0 10px #fff ;
}

</style>