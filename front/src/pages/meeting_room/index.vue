<template>
  <article>
    <h3>例会教室</h3>
    <div id="today-room" class="card">
      今日(
      <span :class="dayColor(todayRoom.date)">
        {{ md(todayRoom.date) }}
      </span>
      )の例会教室は、<br />
      <span id="today-room-name">
        「
        <span :class="roomColor(todayRoom.room)">
          {{ room(todayRoom.room) }}
        </span>
        」
      </span>
      です。
    </div>
    <div id="register" class="card" v-if="registerPermission">
      <h4>教室係用メニュー</h4>
      <router-link
        :to="{ name: 'meeting_room:register' }"
        class="button button-primary"
        >例会教室データの修正・登録 <Icon :icon="['fas', 'edit']"
      /></router-link>
    </div>
    <div id="ical" class="card">
      <h4>Googleカレンダー連携</h4>
      <p>
        Googleカレンダーなどに例会教室データを表示できるようにしました。<br />くわしくはこのボタンから
      </p>
      <router-link
        :to="{ name: 'meeting_room:ical' }"
        class="button button-primary"
        >Googleカレンダー連携の方法 <Icon :icon="['far', 'calendar-plus']"
      /></router-link>
    </div>
    <div id="rooms" class="card">
      <h4>1カ月先までの例会教室一覧</h4>
      <p v-if="rooms.length === 0">Now Loading...</p>
      <table v-else class="pure-table pure-table-bordered">
        <tr v-for="data in rooms" :key="data.date">
          <td>
            <span :class="dayColor(data.date)">
              {{ md(data.date) }}
            </span>
          </td>
          <td>
            <span :class="roomColor(data.room)">
              {{ room(data.room) }}
            </span>
          </td>
        </tr>
      </table>
    </div>
  </article>
</template>

<script setup>
import moment from "@/utils/moment.js";
import axios from "@/utils/axios.js";
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { md, dayColor, room, roomColor } from "./formatter";
const store = useStore();
const registerPermission = computed(
  () => store.state.mypage.userInfo.canRegisterMeetingRoom
);

const rooms = ref([]);

axios.get("/api/meeting_room/get31day/").then((res) => {
  rooms.value = res.data.rooms;
});

const todayRoom = computed(() => {
  const date = moment().format("YYYY-MM-DD");
  const result = rooms.value.find((obj) => obj.date === date);
  if (result === undefined) {
    return {
      date,
      room: null,
    };
  } else {
    return result;
  }
});
</script>

<style lang="scss" scoped>
.card {
  padding: 1rem;
  margin-bottom: 1rem;
  width: 100%;
}
#today-room {
  margin: 1rem auto;
  #today-room-name {
    font-size: 1.2rem;
    line-height: 1.5;
  }
}
h4 {
  display: block;
  margin: 0 0 1rem;
}
#register .button {
  display: inline-block;
  margin: 0;
  padding: 0.75rem;
}
#ical .button {
  display: inline-block;
  margin: 0.5rem 0;
  padding: 0.75rem;
}
.text-danger {
  color: $text-red;
}
.text-primary {
  color: $text-blue;
}
.text-success {
  color: $text-green;
}
.text-muted {
  color: $text-dark;
}
</style>