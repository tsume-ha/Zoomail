<template>
  <article>
    <h3>例会教室</h3>
    <div class="card">
      <router-link
        v-if="isStaff"
        to="./register/"
        id="register"
        class="button button-primary"
        >修正・登録</router-link
      >
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
import { ref } from "vue";
const rooms = ref([]);
const isStaff = false;
axios.get("/api/meeting_room/get31day/").then((res) => {
  rooms.value = res.data.rooms;
});

const md = (date) => moment(date).format("MM/DD (dd)");

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
}
#register {
  display: inline-block;
  margin: 1rem 0;
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