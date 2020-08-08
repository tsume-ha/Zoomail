<template>
  <div>
    <h3>タイトル</h3>
    <calendar-controller
      :displayDays="displayDays"
      @move="move"
      @change-display-days="changeDisplayDays"
    />
    <calendar-table
      :data-list="dataList"
      :display-days="displayDays"
      :current-date="currentDate"
      @update-current-date="updateCurrentDate"
     />

  </div>
</template>

<script>
import moment from 'moment';
import calendarTable from './calendar-table.vue';
import calendarController from './calendar-controller.vue';
export default {
  components: {
    calendarTable,
    calendarController
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
      ],
      displayDays: 5,
      currentDate: moment('2020-05-03'),
    }
  },
  methods: {
    move: function (e) {
      const newdate = moment(this.currentDate.format('YYYY-MM-DD')).add(e, 'days')
      this.currentDate = newdate
    },
    updateCurrentDate: function (e) {
      this.currentDate = e;
    },
    changeDisplayDays: function (e) {
      this.displayDays += e;
    }
  }
}
</script>