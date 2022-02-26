<template>
  <article>
    <h3>例会教室登録・修正</h3>
    <div class="card">
      <form autocomplete="off" class="pure-menu pure-form">
        <h4 class="pure-menu-heading">{{ year }}年{{ month }}月</h4>
        <ul class="pure-menu-list">
          <li v-for="room in rooms" :key="room.date" class="pure-menu-item">
            <div class="date">
              <span :class="dayColor(room.date)">{{ md(room.date) }}</span>
            </div>
            <div class="room">
              <input
                type="text"
                v-model="room.room"
                @change="onChangeHandler(room.date)"
                placeholder="未登録"
                list="rooms-presets"
              />
            </div>
          </li>
          <datalist id="rooms-presets">
            <option value="学生集会所 3階共用室"></option>
            <option value="学生集会所 2階共用室"></option>
            <option value="4共21"></option>
            <option value="4共22"></option>
            <option value="4共24"></option>
            <option value="4共30"></option>
            <option value="4共31"></option>
          </datalist>
        </ul>
      </form>
      <div class="pure-control-group custom-two-buttons-wrapper">
        <button @click="move(-1)" class="pure-button button-primary">
          前の月
        </button>
        <button @click="move(1)" class="pure-button button-primary">
          次の月
        </button>
      </div>
    </div>
    <router-link :to="{ name: 'meeting_room:index' }" class="pure-button return"
      >戻る</router-link
    >
    <div v-if="APIQueue > 0" id="api-saving-text">saving...</div>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import axios from "@/utils/axios.js";
import moment from "@/utils/moment";
import { md, dayColor } from "./formatter";
const store = useStore();
const router = useRouter();

const permission = computed(
  () => store.state.mypage.userInfo.canRegisterMeetingRoom
);
if (!permission.value) {
  store.commit("message/addMessage", {
    level: "warning",
    message: "教室係の権限が無いようです",
    appname: "meeting_room/register",
  });
  router.push({ name: "meeting_room:index" });
}

const today = moment();
const year = ref(today.year());
const month = ref(today.month() + 1);

const rooms = ref([]);
const loading = ref(false);
const getRoomsFromAPI = async (year, month) => {
  loading.value = true;
  const response = await axios.get("/api/meeting_room/get_by_month/", {
    params: {
      year,
      month,
    },
  });
  rooms.value = response.data.rooms;
  loading.value = false;
};

getRoomsFromAPI(year.value, month.value);

const APIQueue = ref(0);
const onChangeHandler = async (date) => {
  // 対象を日付から取得
  const target = rooms.value.find((obj) => obj.date === date);
  // 送信データを作成
  const data = new FormData();
  data.set("date", target.date);
  data.set("room_name", target.room || "");
  // 送信
  APIQueue.value++;
  const response = await axios.post("/api/meeting_room/register/", data);
  APIQueue.value--;
  // 帰ってきたデータを確認
  if (
    !(
      response.data.room === target.room && response.data.date === target.date
    ) &&
    !(target.room === "" && response.data.room === null)
  ) {
    // どっちかが異なる場合
    // 帰ってきたデータで上書きしておく
    rooms.value = [
      ...[...rooms.value].map((obj) =>
        obj.date === target.date ? { ...response.data } : obj
      ),
    ];
    // 警告をだしておく
    store.commit("message/addMessage", {
      level: "warning",
      message: `${target.date}のデータが更新に失敗しました`,
      appname: "meeting_room/register",
    });
  }
};

const move = async (num) => {
  const currentDate = moment([year.value, month.value - 1]);
  currentDate.add(num, "months");
  year.value = currentDate.year();
  month.value = currentDate.month() + 1;
  rooms.value.length = 0;
  await getRoomsFromAPI(year.value, month.value);
};
</script>

<style scoped lang="scss">
.card {
  padding: 0.5rem;
  margin-bottom: 2rem;

  h4 {
    padding: 0.5rem 0 0.75rem;
  }

  ul li div {
    display: inline-block;

    &.date {
      width: 6rem;
    }
    &.room {
      width: calc(100% - 6rem);
      min-width: 10rem;
      input {
        width: 100%;
      }
    }
  }
}

input::placeholder {
  color: $text-dark;
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
#api-saving-text {
  display: block;
  position: fixed;
  bottom: 1rem;
  left: 1rem;
}
</style>