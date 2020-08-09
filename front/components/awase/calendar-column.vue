<template>
  <div class="calendar-column">
    <div class="date" :class="{'sunday': isSunday, 'saturday': isSaturday}">
      {{date.format('M/D')}}
      <br>
      {{date.format('ddd')}}
    </div>
    <div class="room">
      使用不可
    </div>
    <template v-for="h in (displayTimeRange.end - displayTimeRange.begin)">
      <div class="time" :class="(h+displayTimeRange.begin+-1)+'00'" :key="(h+displayTimeRange.begin+-1)+'00'"></div>
      <div class="time" :class="(h+displayTimeRange.begin+-1)+'30'" :key="(h+displayTimeRange.begin+-1)+'30'"></div>
    </template>
  </div>
</template>

<script>
import moment from "moment";
moment.locale('ja', {
  weekdays: ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"],
  weekdaysShort: ["日", "月", "火", "水", "木", "金", "土"],
});
export default {
  props: {
    date: {required: true, type: Object},
    // moment object
    columndata: {required: false, type: Object},
    // {date: "2020-05-01", display_date: "5/1", display_day: "金", weekday: 4, hour_begin: 18},
    displayTimeRange: {required: false, type: Object, default: () => {return {begin:9, end:21}}}
  },
  data: function () {
    return {
    }
  },
  computed: {
    isSaturday: function () {
      return this.date.day() == 6;
    },
    isSunday: function () {
      return this.date.day() == 0;
    }
  }
}
</script>

<style scoped>
.calendar-column{
  display: flex;
  flex-direction: row;
  text-align: center;
}

/* border settings */
.date, .room, .time{
  border-top: 1px solid #eee;
}
.time:last-child{
  border-bottom: 1px solid #eee;
}


.date{
  height: 3.5rem;
  text-align: center;
  line-height: 1.5rem;
  font-size: 12px;
  padding: 0.25rem auto;
}
.date.sunday{
  background-color: #ffc6c6;
}
.date.saturday{
  background-color: rgb(170, 231, 255);
}
.room{
  font-size: 10px;
  text-align: center;
  padding: 5px 0;
  line-height: 15px;
  height: 26px;
  word-break: break-all;
  overflow-x: hidden;
  overflow-y: hidden;
  z-index: 2;
}
.time{
  height: 20px;
}
</style>