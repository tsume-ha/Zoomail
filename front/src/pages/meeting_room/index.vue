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
    <div id="register" class="card" v-if="isStaff">
      <h4>教室係用メニュー</h4>
      <router-link to="./register/" class="button button-primary"
        >例会教室データの修正・登録 <Icon :icon="['fas', 'edit']"
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
const rooms = ref([]);
const isStaff = true;
axios.get("/api/meeting_room/get31day/").then((res) => {
  rooms.value = res.data.rooms;
});

const md = (date) => moment(date).format("M/DD (dd)");

const todayRoom = computed(() => {
  const date = moment().format("YYYY-MM-DD");
  return rooms.value.find((obj) => obj.date === date);
});

const dayColor = (date) => {
  const day = moment(date).format("d");
  if (day === "0") {
    return "text-danger";
  } else if (day === "6") {
    return "text-primary";
  } else {
    return "";
  }
};
const room = (room) => {
  if (room === null) {
    return "例会教室は未登録";
  } else {
    return room;
  }
};
const roomColor = (room) => {
  switch (room) {
    case "終日使用不可":
    case "使用不可":
      return "text-danger";
    case null:
      return "text-muted";
    case "(20時まで音出し不可)":
      return "text-success";
    default:
      return "";
  }
};
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