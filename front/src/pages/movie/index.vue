<template>
  <article>
    <h3>ライブ動画</h3>
    <section v-for="movie in movies" :key="movie.id" class="pure-menu-custom card pure-g">

      <h4 class="pure-menu-heading pure-u-1">
        {{ movie.title }} <time :datetime="movie.heldAt">({{displayDate(movie.heldAt)}})</time>
      </h4>
      
      <div class="youtube pure-u-1" v-if="movie.url">
        <iframe width="560" height="315" class="youtube_content" :src="movie.url" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      </div>

      <div class="pure-u-1" v-if="movie.description" v-html="movie.description"></div>

    </section>
  </article>
</template>

<script setup>
import moment from "@/utils/moment";
import { reactive } from "vue";
import axios from "@/utils/axios";
import { useStore } from "vuex";

const store = useStore();
const movies = reactive([]);

axios.get("/api/movie/").then(res => {
  movies.length = 0;
  movies.push(...res.data.movies);
}).catch(error => {
  console.error(error.response);
  store.commit("message/addMessage", {
    level: "warning",
    message: "ライブ動画のデータを取得できませんでした。",
    appname: "movie/index"
  });
});

const displayDate = dateStr => moment(dateStr).format("YYYY/MM/DD");

</script>

<style lang="scss" scoped>
.card {
  margin-bottom: 0.5rem;
}
.pure-menu-heading {
  border-color: $bg-light;
}
h4 time {
  font-size: 0.75rem;
}

.youtube{
  position: relative;
  display: block;
  width: 100%;
  padding: 56.25% 0 0;
  margin-bottom: 1rem;

  iframe{
    position: absolute;
    top: 0;
    left: 0;
    width: 100% !important;
    height: 100% !important;
  }
}
</style>