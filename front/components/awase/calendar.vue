<template>
  <div>
    <h3>タイトル</h3>
    <calendar-controller
      :displayDays="displayDays"
      @move="move"
      @change-display-days="changeDisplayDays"
    />
    <calendar-table
      :display-days="displayDays"
      :current-date="currentDate"
      :displayTimeRange="{begin: timeRangeBegin, end: timeRangeEnd}"
      :schedule-data="dataList"
      @update-current-date="updateCurrentDate"
      @days-for-time-range-calc="updateCurrentDateNumForTimeRangeCalc"
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
        // {date: "2020-05-01", hour_begin: 18, hour_end: 26,
        //  schedule_list: {hoge:{9_00: true, 9_30: false},
        //                  fuga:{9_00: true, 9_30: true}
        //                 },
      ],
      displayDays: 5,
      currentDate: moment('2020-08-24'),
      currentDateNumForTimeRangeCalc: 5,
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
    },
    updateCurrentDateNumForTimeRangeCalc(e) {
      this.currentDateNumForTimeRangeCalc = e;
    }
  },
  computed: {
    displayingDays: function () {
    // Scheduleデータのうち、表示中のものを抽出してreturn
      let result = [];
      for (let i = 0; i < this.displayDays; i++) {
        let date = moment(this.currentDate.format('YYYY-MM-DD')).add(
          i - this.displayDays + this.currentDateNumForTimeRangeCalc,
          'days'
          );
        let _result = this.dataList.find(e => e['date'] == date.format('YYYY-MM-DD'));
        if (_result != undefined) {
          result.push(_result);
        }
      }
      return result;
    },
    timeRangeBegin: function () {
      if (this.displayingDays.length == 0) {
        return 18;
      }
      let values = [];
      for (let i = 0; i < this.displayingDays.length; i++) {
        values.push(this.displayingDays[i].hour_begin);
      }
      return Math.max(Math.min(...values), 9);
    },
    timeRangeEnd: function () {
      if (this.displayingDays.length == 0) {
        return 24;
      }
      let values = [];
      for (let i = 0; i < this.displayingDays.length; i++) {
        values.push(this.displayingDays[i].hour_end);
      }
      return Math.min(Math.max(...values), 26);
    }
  },
  created: function () {
    this.axios
    .get('./json/')
    .then(res => {
      console.log(res.data.calendar_data)
      this.dataList = res.data.calendar_data;
    })
  },
}
</script>