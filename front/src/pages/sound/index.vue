<template>
  <article>
    <h3>リハ音源</h3>
    <div v-if="soundStaff" v-cloak>
      <a href="/admin/sound/live/" target="_blank">編集はこちらから</a>
    </div>

    <div class="pure-g">
      <div
        v-for="live in lives" :key="'live-' + live.id"
        class="pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3 card-wrapper"
      >
        <router-link :to="{name: 'sound:content', params: {id: live.id}}">
          <article class="card card-sound">
            <h4 class="card-title">{{ live.title }}</h4>
            <time :data-date="live.date" class="small">Recorded : {{ displayDate(live.date) }}</time>
            <p class="songdetail">
              <span v-for="song in live.songs" :key="'song-' + song.id">
                {{ song.trackNum }}. {{ song.title }}
              </span>
            </p>
            <span class="small">ほか、全{{ live.songs.length }}曲</span>
          </article>
        </router-link>
      </div>
    </div>
  </article>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import moment from "../../utils/moment";
export default {
  setup() {
    const store = useStore();
    const lives = computed(() => store.state.sound.lives);

    store.dispatch("sound/getSoundsFromAPI").catch(error => {
      if (error.message == "Network Error" && error.response === undefined) {
        console.log("通信エラー");
      } else if (error.response.status === 500) {
        console.log("500");
      // } else if (error.response.status === 403){
      // } else if (error.response.status === 404){
      // } else {
      //   console.log(error.message);
      }
    });
    const displayDate = dateStr => moment(dateStr).format("YYYY/MM/DD (ddd)");
    const soundStaff = computed(() => store.state.user.is_staff);

    return {
      lives, soundStaff,
      displayDate
    };
  },
};
</script>

<style lang="scss" scoped>
.card-wrapper{
  padding: .5rem;
  margin: 0;
  align-items: stretch;

  :hover {
    text-decoration: none;
    background-color: #e4f4f8;
    h4 {
      text-decoration: underline;
    }
  }

  .card-sound{
    padding: .5rem;
    margin: 0;
    height: 100%;
    > * {
      display: block;
      width: 100%;
      margin: .25rem 0 0;
    }

    time {
      text-align: right;
    }
    .songdetail {
      flex-grow: 1;

      span {
        margin-right: 1rem;
      }
    }


  }

}
</style>