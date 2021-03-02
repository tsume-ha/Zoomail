<template>
  <div>
    <row
      v-for="room in rooms" :key="room.date"
      :data="room"
      :selected="Boolean(room.date in selectedDate)"
      @dayadd="dayadd"
      @dayremove="dayremove"
      @oninput="oninput"
    />
    <datalist id="room-choices">
      <option value="4共21" />
      <option value="4共22" />
      <option value="終日使用不可" />
    </datalist>
  </div>
</template>

<script>
import row from "./register-column-row";
export default {
  metaInfo: {
    title: '教室係用ページ - 例会教室'
  },
  components: {
    row
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
      let id = e.format('YYYY-MM-DD');
      if (!(id in this.selectedDate)) {
        this.$set(this.selectedDate, id, e);
      }
    },
    dayremove: function(e){
      let id = e.format('YYYY-MM-DD');
      if (id in this.selectedDate) {
        this.$delete(this.selectedDate, id);
      }
    },
    oninput (payload) {
      const targetIndex = this.rooms.indexOf(
        this.rooms.find(item=>item.date == payload.date)
      )
      this.$set(this.rooms, targetIndex, payload)
      this.$set(this.queue, payload.date, payload)
    }
  }
}
</script>

<style scoped>
</style>