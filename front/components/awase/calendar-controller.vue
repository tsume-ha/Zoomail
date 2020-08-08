<template>
  <div id="calendar-conroller" class="row mx-0 my-2 clearfix">
    <div id="controller_days" class="float-left">
      <button @click="changeDisplayDays(-1)"><img src="/static/img/awase/red.png" height="24" alt="列を減らす"><span>列を</span><span>減らす</span></button>
      <button @click="changeDisplayDays(1)"><img src="/static/img/awase/add.png" height="24" alt="列を増やす"><span>列を</span><span>増やす</span></button>
    </div>
    <div id="controller_move" class="float-right">
      <button @click="move(-displayDays)"><img src="/static/img/awase/1w_bk.png" height="24" :alt="displayDays">{{displayDays}}日戻る</button>
      <button @click="move(-1)"><img src="/static/img/awase/1d_bk.png" height="24" alt="1日戻る">1日戻る</button>
      <button @click="move(1)"><img src="/static/img/awase/1d_fw.png" height="24" alt="1日進む">1日進む</button>
      <button @click="move(displayDays)"><img src="/static/img/awase/1w_fw.png" height="24" :alt="displayDays">{{displayDays}}日進む</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    displayDays: {required: true, type: Number}
  },
  methods: {
    move: function (days) {
      this.$emit('move', days)
    },
    changeDisplayDays: function (diff) {
      this.$emit('change-display-days', diff)
    }
  }
}
</script>

<style scoped>
#calendar-conroller{
  display: block;
  position: relative;
}
#calendar-conroller div{
  display: inline-block;
  position: relative;
}
#calendar-conroller div button{
  display: inline-block;
  position: relative;
  background-color: #fff;
  border-style: none;
  text-align: center;
  font-size: 10px;
  margin: 0;
  padding: 0 4px;
}
#calendar-conroller div button img{
  display: block;
  margin: 0 auto;
}
#calendar-conroller div button span{
  display: inline-block;
  white-space: nowrap;
}

@media screen and (min-width: 340px) {/*340px以上*/
div#controller_days button{
  width: 58px;
}
}
@media screen and (max-width: 339px) {/*339px以下*/
div#controller_days button{
  width: 38px;
}
} 

</style>