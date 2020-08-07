<template>
  <div id="calendar-carousel">
    <div class="calendar-column" :style="[columnWidth]">1</div>
    <div class="calendar-column" :style="[columnWidth]">2</div>
    <div class="calendar-column" :style="[columnWidth]">3</div>
    <div class="calendar-column" :style="[columnWidth]">4</div>
    <div class="calendar-column" :style="[columnWidth]">5</div>
    <div class="calendar-column" :style="[columnWidth]">6</div>
    <div class="calendar-column" :style="[columnWidth]">7</div>
    <div class="calendar-column" :style="[columnWidth]">8</div>
    <div class="calendar-column" :style="[columnWidth]">9</div>
    <div class="calendar-column" :style="[columnWidth]">10</div>
    <div class="calendar-column" :style="[columnWidth]">{{columnWidth}}</div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      displayDays: 5,
      carouselWidth: 100,
    }
  },
  mounted () {
    this.carouselWidth = this.$el.clientWidth;
  },
  computed: {
    columnWidth: function () {
      // 15px 分は .container のpaddingを打ち消すために
      return {width: (this.carouselWidth - 15) / this.displayDays + 'px'};
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
}
#calendar-carousel .calendar-column{
  display: inline-block;
  margin: 0;
  padding: 0;
  border-right: 1px solid #eee;
}
</style>