<template>
  <div class="mb-5">
    <row
      v-for="room in rooms" :key="room.date"
      :data="room"
      :notselected="multipleMode && (!Boolean(room.date in selectedDate))"
      @dayclicked="dayclicked"
      @oninput="oninput"
    />
    <datalist id="room-choices">
      <option value="4共21" />
      <option value="4共22" />
      <option value="終日使用不可" />
    </datalist>

    <div
      v-if="canSend || multipleMode"
      class="send-menu container"
    >
      <div class="row mb-3 mt-2">
        <div class="col-sm-6">
          <button
            v-if="multipleMode"
            @click="selectedDate={}"
            class="btn btn-sm btn-secondary"
            >選択を解除する</button>
        </div>
        <div class="col-sm-6">
          <button
            v-if="canSend"
            @click=""
            class="btn btn-info"
            >送信</button>
        </div>
      </div>
    </div>

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
    queue: {},
    selectedDate: {},

    // 画面表示用データ
    nowLoading: false,
    displayNum: 0,
      // 0 => 1日ごと選択
      // 1 => 範囲で選択

  }),
  computed: {
    multipleMode () {
      // 一括変更モード Boolean
      return Object.keys(this.selectedDate).length > 0;
    },
    canSend () {
      return Object.keys(this.queue).length > 0;
    }
  },
  created () {
    this.axios.get('/api/meeting_room/get_all/')
    .then(res => {
      this.rooms = res.data.rooms;
    })
  },
  //props.day.date
  methods: {
    dayclicked: function(e){
      let id = e.format('YYYY-MM-DD');
      if (id in this.selectedDate) {
        this.$delete(this.selectedDate, id);
      } else {
        this.$set(this.selectedDate, id, e);
      }
    },
    dayremove: function(e){
      let id = e.format('YYYY-MM-DD');
      if (id in this.selectedDate) {
        
      }
    },
    oninput (payload) {
      let dates = [];
      if (this.multipleMode){
        dates = Object.keys(this.selectedDate);
      } else {
        dates = [payload.date];
      }
      for (const date of dates) {
        const tmp = {
          "date": date,
          "room": payload.room
        };
        const targetIndex = this.rooms.indexOf(
          this.rooms.find(item=>item.date == date)
        );
        this.$set(this.rooms, targetIndex, tmp);
        this.$set(this.queue, date, tmp);
      }
      // selectedDateを初期化
      this.selectedDate = {};
    }
  }
}
</script>

<style scoped>
.send-menu{
  position: fixed;
  display: block;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(255, 255, 255, 0.6);
  border-top: 0.25rem #fff solid;
}
</style>