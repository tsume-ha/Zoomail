<template>
    <div id="calendar-table">
      <calendar-leftside />
      <calendar-carousel
        :data-list="dataList" />
    </div>
</template>

<script>
import calendarLeftside from './calendar-leftside.vue';
import calendarCarousel from './calendar-carousel.vue';
export default {
  components: {
    calendarLeftside,
    calendarCarousel
  },
  data: function () {
    return {
      dataList: [
        {date: "2020-05-01", display_date: "5/1", display_day: "金", weekday: 4, hour_begin: 18},
        {date: "2020-05-02", display_date: "5/2", display_day: "土", weekday: 5, hour_begin: 9},
        {date: "2020-05-03", display_date: "5/3", display_day: "日", weekday: 6, hour_begin: 9},
        {date: "2020-05-04", display_date: "5/4", display_day: "月", weekday: 0, hour_begin: 9},
        {date: "2020-05-05", display_date: "5/5", display_day: "火", weekday: 1, hour_begin: 9},
        {date: "2020-05-06", display_date: "5/6", display_day: "水", weekday: 2, hour_begin: 9},
        {date: "2020-05-07", display_date: "5/7", display_day: "木", weekday: 3, hour_begin: 9},
        {date: "2020-05-08", display_date: "5/8", display_day: "金", weekday: 4, hour_begin: 18},
        {date: "2020-05-09", display_date: "5/9", display_day: "土", weekday: 5, hour_begin: 9},
      ]
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