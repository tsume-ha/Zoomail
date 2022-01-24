<template>
  <article class="cancel-parent-container">
    <div class="logo-wraper">
      <img id="logo" class="pure-img" src="@/assets/img/zoomail.png" />
    </div>
    <p>
      <span>京都大学を中心に活動する</span
      ><span>アコースティック軽音サークル</span><br />
      <span
        >「<a href="https://ku-unplugged.net" target="_blank"
          >京大アンプラグド</a
        >」</span
      ><span>の部内連絡管理アプリ</span>
    </p>

    <div id="top-info" class="container">
      <div class="pure-g">
        <section class="pure-menu-custom pure-u-1 pure-u-md-1-2">
          <h4 class="pure-menu-heading">New Contents</h4>
          <ul class="pure-menu-list">
            <li
              v-for="item in newContents"
              :key="item.id"
              class="pure-menu-item"
            >
              <router-link :to="item.path" class="pure-menu-link">
                【{{ item.genre }}】 {{ item.title }}
              </router-link>
            </li>
          </ul>
        </section>
        <section class="pure-menu-custom pure-u-1 pure-u-md-1-2">
          <h4 class="pure-menu-heading">Announcements</h4>
          <ul class="pure-menu-list">
            <li
              v-for="item in announcements"
              :key="item.id"
              class="pure-menu-item"
            >
              <div class="announcement-content">
                <time class="small">{{ item.date }}</time> {{ item.text }}
              </div>
            </li>
          </ul>
        </section>
      </div>
    </div>
  </article>
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import axios from "../../utils/axios";
export default {
  setup() {
    const store = useStore();
    const newContents = ref([]);
    const announcements = ref([]);
    onMounted(() => {
      axios
        .get("/api/home/index/")
        .then((res) => {
          newContents.value = res.data.newContents;
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
      newContents,
      announcements,
    };
  },
};
</script>

<style lang="scss" scoped>
article {
  min-height: calc(100vh - 3rem - (1rem + 0.75rem * 1.25));
  background-image: linear-gradient(
      rgba(56, 100, 113, 0.8),
      rgba(56, 100, 113, 0.8)
    ),
    url("@/assets/img/LP-BG.jpeg");
  background-repeat: no-repeat;
  background-size: cover;
  text-shadow: 0 0 0.25rem #000;

  .logo-wraper {
    display: block;
    max-width: 400px;
    margin: 1rem auto;
  }

  p {
    color: $text-white;
    text-align: center;
    > * {
      display: inline-block;
    }
  }

  div#top-info {
    color: $text-white;
    margin-top: 3rem;
    .pure-menu-heading {
      border-color: $text-white !important;
    }
    .announcement-content {
      padding: 0.5em 1em;
      line-height: 1.5;
      time {
        padding: 0 0.5rem;
      }
    }
  }
}
</style>