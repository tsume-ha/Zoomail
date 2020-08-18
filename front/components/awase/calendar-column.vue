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
      <div class="time" :class="[CountNGNumber((h+displayTimeRange.begin-1)+'_0')]" :key="(h+displayTimeRange.begin-1)+'00'"></div>
      <div class="time" :class="[CountNGNumber((h+displayTimeRange.begin-1)+'_30')]" :key="(h+displayTimeRange.begin-1)+'30'"></div>
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
    columndata: {required: false, type: Object, default: ()=>{return {schedule_list: ''}}},
    displayTimeRange: {required: true, type: Object}
  },
  data: function () {
    return {
      className: ['NG0', 'NG1', 'NG2', 'NG3'],
    }
  },
  computed: {
    isSaturday: function () {
      return this.date.day() == 6;
    },
    isSunday: function () {
      return this.date.day() == 0;
    },
    hasScheduleData: function () {
      const keys = Object.keys(this.columndata.schedule_list);
      for (const key of keys) {
        if (Object.keys(this.columndata.schedule_list[key]).length > 0) {
          return true;
        }
      }
      return false;
    }
  },
  methods: {
    CountNGNumber: function (time) {// time: str, example: '18_0', '18_30'
      if (!this.hasScheduleData) {
        return '';
      }
      const user_names = Object.keys(this.columndata.schedule_list);
      let count = 0;
      let flag = false;
      for (const user_name of user_names) {
        if (this.columndata.schedule_list[user_name][time] === false) {
          count += 1;
          flag = true;
        } else if (this.columndata.schedule_list[user_name][time] === true) {
          flag = true;
        }
      }
      if (!flag) {
        return ''
      } else {
        if (count > 3) {
          return this.className[3]
        } else {
          return this.className[count];
        }
      }
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
@import "./calendar-table-cell.css";
@import "./calendar-color.css";
.date.sunday{
  background-color: #ffc6c6;
}
.date.saturday{
  background-color: rgb(170, 231, 255);
}

</style>