<template>
  <div id="calendar-carousel">
    <div class="calendar-column" :style="[columnStyle]">1</div>
    <div class="calendar-column" :style="[columnStyle]">2</div>
    <div class="calendar-column" :style="[columnStyle]">3</div>
    <div class="calendar-column" :style="[columnStyle]">4</div>
    <div class="calendar-column" :style="[columnStyle]">5</div>
    <div class="calendar-column" :style="[columnStyle]">6</div>
    <div class="calendar-column" :style="[columnStyle]">7</div>
    <div class="calendar-column" :style="[columnStyle]">8</div>
    <div class="calendar-column" :style="[columnStyle]">9</div>
    <div class="calendar-column" :style="[columnStyle]">10</div>
    <div class="calendar-column" :style="[columnStyle]">11</div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      displayDays: 5,
      carouselWidth: 100,
      diffX: 0,
    }
  },
  computed: {
    columnStyle: function () {
      return {
        width: 100 / this.displayDays + '%',
        transform: 'translate3d(' + this.diffX + 'px, 0, 0)'};
    }
  }
}
</script>

<style scoped>
#calendar-carousel{
  background-color: rgb(255, 137, 137);
  white-space: nowrap;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
  position: relative;
  font-size: 0;/* inline-blockのとき隙間が空くので指定 */
}
#calendar-carousel .calendar-column{
  display: inline-block;
  margin: 0;
  padding: 0;
  font-size: 16px;/* 親要素に0をしていしたので戻す */
  border-right: 1px solid #eee;
}
</style>