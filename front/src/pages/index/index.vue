<template>
  <article class="cancel-parent-container">
    <div class="logo-wraper">
      <img id="logo" class="pure-img" src="@/assets/img/zoomail.png" />
    </div>
    <p>
      京都大学を中心に活動するアコースティック軽音サークル<br />
      「<a href="https://ku-unplugged.net" target="_blank">京大アンプラグド</a
      >」の部内連絡管理アプリ
    </p>
  </article>
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import axios from "../../utils/axios";
export default {
  setup() {
    const store = useStore();
    const contentLog = ref([]);
    const announcements = ref([]);
    onMounted(() => {
      axios
        .get("/api/home/index/")
        .then((res) => {
          console.log(res.data);
          contentLog.value = res.data.contentLog;
          announcements.value = res.data.announcements;
        })
        .catch((err) => {
          store.commit("message/addMessage", {
            level: "error",
            message: `${String(err.response.status)} ${
              err.response.statusText
            }`,
            appname: "index/index",
          });
          console.error(err.response);
        });
    });

    return {
      contentLog,
      announcements,
    };
  },
};
</script>

<style lang="scss" scoped>
article {
  text-align: center;
  background-image: linear-gradient(
      rgba(56, 100, 113, 0.8),
      rgba(56, 100, 113, 0.8)
    ),
    url("@/assets/img/LP-BG.jpeg");
  background-repeat: no-repeat;
  background-size: cover;

  .logo-wraper {
    display: block;
    max-width: 400px;
    margin: 1rem auto;
  }

  p {
    text-shadow: 0 0 0.25rem #000;
    color: $text-white;
  }
}
</style>