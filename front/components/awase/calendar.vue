<template>
  <div>
    <div>
      <a id="return" href="../" class="float-left col-xs-2"> </a>
      <h4 id="title">{{title}}</h4>
      </div>
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
      @show-detail="showDetail"
    />
    <calendar-detail
      v-if="selected.isActive"
      :data-list="dataList"
      :date="selected.date"
      :hour="selected.hour"
      :minute="selected.minute"
      @close-detail="closeDetail"
    />
  </div>
</template>

<script>
import moment from 'moment';
import calendarTable from './calendar-table.vue';
import calendarController from './calendar-controller.vue';
import calendarDetail from './calendar-detail.vue';
export default {
  components: {
    calendarTable,
    calendarController,
    calendarDetail
  },
  data: function () {
    return {
      title: '',
      dataList: [
        // {date: "2020-05-01", hour_begin: 18, hour_end: 26,
        //  schedule_list: {taro:{9_00: true, 9_30: false},
        //                  jiro:{9_00: true, 9_30: true}
        //                 },
      ],
      displayDays: 5,
      currentDate: moment('2020-08-24'),
      selected: {
        isActive: false,
        date: moment('2020-08-28'),
        hour: 12,
        minute: 0,
      }
    }
  },
  methods: {
    move: function (e) {
      this.currentDate = this.currentDate.clone().add(e, 'days');
    },
    updateCurrentDate: function (e) {
      this.currentDate = e;
    },
    changeDisplayDays: function (e) {
      this.displayDays += e;
    },
    showDetail: function (e) {
      this.$set(this.selected, 'isActive', true);
      this.$set(this.selected, 'date', e.date);
      this.$set(this.selected, 'hour', e.hour);
      this.$set(this.selected, 'minute', e.minute);
    },
    closeDetail: function () {
      this.$set(this.selected, 'isActive', false);
    }
  },
  computed: {
    timeRangeBegin: function () {
      if (this.dataList.length == 0) {
        return 18;
      }
      let values = [];
      for (let i = 0; i < this.dataList.length; i++) {
        values.push(this.dataList[i].hour_begin);
      }
      return Math.max(Math.min(...values), 9);
    },
    timeRangeEnd: function () {
      if (this.dataList.length == 0) {
        return 24;
      }
      let values = [];
      for (let i = 0; i < this.dataList.length; i++) {
        values.push(this.dataList[i].hour_end);
      }
      return Math.min(Math.max(...values), 26);
    }
  },
  created: function () {
    this.axios
      .get('./json/')
      .then(res => {
        this.dataList = res.data.calendar_data;
      });
    this.axios
      .get('./api/info/')
      .then(res => {
        this.title = res.data.title;
        const today = moment();
        if (today.diff(moment(res.data.days_begin)) < 0) {
          this.currentDate = moment(res.data.days_begin);
        } else if (today.diff(moment(res.data.days_end)) > 0) {
          this.currentDate = moment(res.data.days_end).subtract(this.displayDays-1, 'days');
        } else {
          this.currentDate = today;
        }
      });
  },
}
</script>

<style scoped>
#return{
  height:24px;
  width:24px;
  display:block;
  position:relative;
  overflow:hidden;
  margin: 3px;
}
#return:before{
  content:'';
  height:12px;
  width:12px;
  display:block;
  border:1px solid #333;
  border-right-width:0;
  border-bottom-width:0;
  transform:rotate(-45deg);-webkit-transform:rotate(-45deg);-moz-transform:rotate(-45deg);-o-transform:rotate(-45deg);-ms-transform:rotate(-45deg);
  position:absolute;
  top:5px;
  left:5px;
}
#return:after{
  content:'';
  height:1px;
  width:20px;
  display:block;
  background:#333;
  position:absolute;
  top:10.5px;
  left:3px;
}
h4#title{
  display: inline-block;
  margin-left: 0.5rem;
}
</style>