<template>
  <article>
    <h3>その他資料</h3>
    <section class="pure-menu-custom card">
      <ul class="pure-menu-list pure-g">
        <li
          class="pure-menu-item others-content pure-u-1"
          v-for="content in contents"
          :key="content.id"
        >
          <div>
            <a :href="`/download/others/${content.id}/`" target="_blank">
              {{ content.title }}
            </a>
          </div>
          <p v-if="content.detail" class="small">
            {{ content.detail }}
          </p>
        </li>
      </ul>
    </section>
  </article>
</template>

<script setup>
// import moment from "@/utils/moment";
import { reactive } from "vue";
import axios from "@/utils/axios";
import { useStore } from "vuex";

const store = useStore();
const contents = reactive([]);

axios
  .get("/api/others/")
  .then((res) => {
    contents.length = 0;
    contents.push(...res.data.contents);
  })
  .catch((error) => {
    console.error(error.response);
    store.commit("message/addMessage", {
      level: "warning",
      message: "その他資料のデータを取得できませんでした。",
      appname: "others/index",
    });
  });

// const displayDate = (dateStr) => moment(dateStr).format("YYYY/MM/DD hh:mm");
</script>

<style lang="scss" scoped>
.card {
  margin-bottom: 0.5rem;
}
.others-content {
  margin: 0.75rem 0;

  > * {
    display: block;
    width: 100%;
  }
}
</style>