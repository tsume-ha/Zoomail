<template>
  <div id="calendar-carousel" @mousedown="onMouseDown">
    <div
      v-for="columndata in dataList"
      :key="columndata.date"
      class="calendar-column"
      :style="[columnStyle]"
    >
      {{columndata.display_date}}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dataList: {required: true, type: Array},
  },
  data: function () {
    return {
      displayDays: 5,
      startX: null,
      diffX: 0,
      currentNum: 0,
    }
  },
  computed: {
    columnStyle: function () {
      return {
        width: 100 / this.displayDays + '%',
        transform: `
          translate3d(${this.diffX}px, 0, 0)
          translate3d(${this.currentNum * (-100)}%, 0, 0)`
      }
    }
  },
  mounted: function () {
    window.addEventListener('mousemove', this.onMouseMove);
    window.addEventListener('mouseup', this.onMouseUp);
  },
  beforeDestroy: function () {
    window.removeEventListener('mousemove', this.onMouseMove);
    window.removeEventListener('mouseup', this.onMouseUp);
  },
  methods: {
    onMouseDown(e) {
      this.startX = e.clientX;
    },
    onMouseMove(e) {
      if (this.startX == null) {
        return;
      }
      this.diffX = e.clientX - this.startX;
    },
    onMouseUp(e) {
      this.startX = null;
      // if (this.diffX > 20) {
      //   this.currentNum = Math.max(this.currentNum - 1, 0);
      // }
      // if (this.diffX < -20) {
      //   this.currentNum = Math.min(this.currentNum + 1, 1);
      // }
      this.diffX = 0;
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