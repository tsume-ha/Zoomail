<template>
  <span id="back" @click="onclick"> </span>
</template>
<script>
module.exports = {
  name: "router-back-arrow",
  props: {
    href: {type: String, required: false, default: '../'}
  },
  methods: {
    onclick () {
      console.log('link clicked')
      this.$router.push(this.href)
    }
  }
};
</script>
<style scoped>
#back{
  height: 24px;
  width: 24px;
  display: inline-block;
  position: relative;
  overflow: hidden;
  margin: 3px 0.5rem 3px 0.25rem;
}
#back:before{
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
#back:after{
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