<template>
  <div id="back">
    <span @click="onclick"> </span>
  </div>
</template>
<script>
module.exports = {
  name: "router-back-arrow",
  props: {
    href: {type: String, required: false, default: '../'}
  },
  methods: {
    onclick () {
      if (this.sendboxMode){
        return this.$router.push('/mypage/sendbox/')
      }
      this.$router.push(this.href)
    }
  },
  computed: {
    sendboxMode () {
      return this.$store.state.read.sendboxMode;
    }
  }
};
</script>
<style scoped>
div#back{
  display: inline-block;
  
  height: 24px;
  margin: 0 6px 0 0;
}

#back > span{
  height: 24px;
  width: 24px;
  display: inline-block;
  position: relative;
  overflow: hidden;
  margin: 0;
}
#back > span:before{
  content: '';
  height: 12px;
  width: 12px;
  display: block;
  border: 1px solid #333;
  border-right-width: 0;
  border-bottom-width: 0;
  transform: rotate(-45deg);
  position: absolute;
  top: 5px;
  left: 5px;
}
#back > span:after{
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