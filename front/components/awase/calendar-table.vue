<template>
    <div id="calendar-table">
      <calendar-leftside
        :display-time-range="displayTimeRange"
      />
      <calendar-carousel
        :data-list="dataList"
        :display-days="displayDays"
        :current-date="currentDate"
        :display-time-range="displayTimeRange"
        @update-current-date="updateCurrentDate"
      />
    </div>
</template>

<script>
import moment from "moment"
import calendarLeftside from './calendar-leftside.vue';
import calendarCarousel from './calendar-carousel.vue';
export default {
  components: {
    calendarLeftside,
    calendarCarousel
  },
  props: {
    dataList: {required: true, type: Array},
    displayDays: {required: true, type: Number},
    currentDate: {required: true, type: Object},
    displayTimeRange: {required: false, type: Object, default: () => {return {begin:9, end:21}}}
  },
  methods: {
    updateCurrentDate(e) {
      this.$emit('update-current-date', e)
    }
  }
}
</script>

<style scoped>
#calendar-table{
  display: flex;
  flex-direction: row;
  position: relative;
  box-sizing: border-box;
}
#calendar-table > div{
  position: relative;
  margin: 0;
  padding: 0;
}
#calendar-table > #calendar-leftside{
  display: inline-block;
  flex-basis: 40px;
  flex-shrink: 0;
  flex-grow: 0.25;
}
#calendar-table > #calendar-carousel{
  display: inline-block;
  flex-basis: auto;
  flex-shrink: 1;
  flex-grow: 10;
}
</style>