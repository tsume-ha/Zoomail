<template>
  <div id="calendar-carousel" @mousedown="onMouseDown">
    <calendar-column
      v-for="i in daysRange"
      :key="getDate(i - displayDays - 1).format('YYYY-MM-DD')"
      :date="getDate(i - displayDays - 1)"
      :columndata="getScheduleData(getDate(i - displayDays - 1))"
      :style="[columnStyle, isTransition]"
    />
  </div>
</template>

<script>
import moment, { relativeTimeThreshold } from 'moment'
import calendarColumn from './calendar-column.vue'
export default {
  props: {
    dataList: {required: true, type: Array},
    displayDays: {required: true, type: Number},
    currentDate: {required: true, type: Object},
  },
  components: {
    calendarColumn,
  },
  data: function () {
    return {
      startX: null,
      diffX: 0,
      currentNum: 0,
      isAnimating: true,
    }
  },
  computed: {
    daysRange: function () {
      return this.displayDays * 3;
    },
    columnStyle: function () {
      return {
        width: 100 / this.displayDays + '%',
        transform: `
          translate3d(${this.diffX}px, 0, 0)
          translate3d(${this.currentNum * (-100)}%, 0, 0)`
      }
    },
    isTransition: function () {
      if (this.isAnimating) {
        return {transition: '0.2s'}
      } else {
        return {transition: 'none'}
      }
    }
  },
  mounted: function () {
    window.addEventListener('mousemove', this.onMouseMove);
    window.addEventListener('mouseup', this.onMouseUp);

    // 前後に用意してある分ずらす
    this.currentNum = this.displayDays;
  },
  beforeDestroy: function () {
    window.removeEventListener('mousemove', this.onMouseMove);
    window.removeEventListener('mouseup', this.onMouseUp);
  },
  methods: {
    getDate(diff) {
      let current = moment(this.currentDate.format('YYYY-MM-DD'));
      return current.add(diff, 'days');
    },
    getScheduleData(date) {
      return this.dataList.find(e => e['date'] == date.format('YYYY-MM-DD'));
    },
    onMouseDown(e) {
      this.isAnimating = false;
      this.reconstruct();
      this.startX = e.clientX;
    },
    onMouseMove(e) {
      if (this.startX == null) {
        return;
      }
      this.diffX = e.clientX - this.startX;
    },
    onMouseUp(e) {
      this.isAnimating = true;
      this.startX = null;
      const columnwidth = this.$el.clientWidth / this.displayDays;
      const diffDays = -1 * Math.round(this.diffX / columnwidth);
      this.currentNum += diffDays
      this.diffX = 0;
    },
    reconstruct() {
      const diffDays = this.currentNum - this.displayDays;
      const newdate = this.getDate(diffDays);
      this.$emit('update-current-date', newdate);
      this.currentNum = this.displayDays;
    }
  }
}
</script>

<style scoped>
#calendar-carousel{
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