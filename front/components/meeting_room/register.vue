<template>
  <div class="calendar-wraper">
    <v-calendar
      :first-day-of-week="2"
      is-expanded
      :columns="$screens({ default: 1, lg: 2 })"
      >
      <template slot='header-title' slot-scope='props'>
        {{props.yearLabel}}年{{props.monthLabel}}
      </template>
      <template slot='day-content' slot-scope='props'>
        <custom-day-content
          :day="props.day"
          :data="rooms.find(x=>x['date'] == props.day.id)"
          :is-selected="(props.day.id in selectedDate)"
          @dayadd="dayadd"
          @dayremove="dayremove"
          ></custom-day-content>
      </template>

    </v-calendar>
  </div>
</template>

<script>
import Calendar from 'v-calendar/lib/components/calendar.umd';
import registerCustomDayContent from './register-custom-day-content.vue';
// import { methods } from '../board/router-back-arrow.vue';
export default {
  metaInfo: {
    title: '教室係用ページ - 例会教室'
  },
  components: {
    customDayContent: registerCustomDayContent,
    "v-calendar": Calendar,
  },
  data: () => ({
    // 内部データ
    rooms: [],
    queue: [],
    selectedDate: {},

    // 画面表示用データ
    nowLoading: false,
    displayNum: 0,
      // 0 => 1日ごと選択
      // 1 => 範囲で選択

  }),
  created () {
    this.axios.get('/api/meeting_room/get_all/')
    .then(res => {
      this.rooms = res.data.rooms;
    })
  },
  //props.day.date
  methods: {
    dayadd: function(e){
      let id = e.id;
      if (!(id in this.selectedDate)) {
        this.$set(this.selectedDate, id, e);
      }
    },
    dayremove: function(e){
      let id = e.id;
      if (id in this.selectedDate) {
        this.$delete(this.selectedDate, id);
      }
    },
  }
}
</script>

<style scoped>
.calendar-wraper{
  max-width: 100%;
  overflow-x: scroll;
}
</style>