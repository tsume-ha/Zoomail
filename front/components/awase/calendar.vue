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
      :displayTimeRange="{begin: timeRangeBegin, end: timeRangeEnd}"
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
        {date: "2020-05-01", hour_begin: 18, hour_end: 26},
        {date: "2020-05-02", hour_begin: 12, hour_end: 26},
        {date: "2020-05-03", hour_begin: 12, hour_end: 26},
        {date: "2020-05-04", hour_begin: 10, hour_end: 26},
        {date: "2020-05-05", hour_begin: 12, hour_end: 26},
        {date: "2020-05-06", hour_begin: 12, hour_end: 26},
        {date: "2020-05-07", hour_begin: 12, hour_end: 26},
        {date: "2020-05-08", hour_begin: 18, hour_end: 26},
        {date: "2020-05-09", hour_begin: 9, hour_end: 26},
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
  },
  computed: {
    displayingDays: function () {
      let result = [];
      for (let i = 0; i < this.displayDays; i++) {
        let date = moment(this.currentDate.format('YYYY-MM-DD')).add(i, 'days');
        let _result = this.dataList.find(e => e['date'] == date.format('YYYY-MM-DD'));
        if (_result != undefined) {
          result.push(_result);
        }
      }
      return result;
    },
    timeRangeBegin: function () {
      let values = [];
      for (let i = 0; i < this.displayingDays.length; i++) {
        values.push(this.displayingDays[i].hour_begin);
      }
      return Math.min(...values);
    },
    timeRangeEnd: function () {
      let values = [];
      for (let i = 0; i < this.displayingDays.length; i++) {
        values.push(this.displayingDays[i].hour_end);
      }
      return Math.max(...values);
    }
  }
}
</script>