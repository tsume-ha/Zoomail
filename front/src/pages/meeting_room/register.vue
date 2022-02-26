<template>
  <article>
    <h3>例会教室登録・修正</h3>
  </article>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
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
</script>