<template>
<div>
  <h3>リハ音源</h3>
  <div class="row" v-if="soundStaff" v-cloak>
    <a href="/admin/sound/live/">編集はこちらから</a>
  </div>
  <section class="row">
    <div v-for="live in lives" :key="'live-' + live.id" class="cardwrap col-xs-12 col-sm-12 col-md-6 col-lg-4">
      <article class="card m-2">
        <router-link :to="{name: 'sound:content', params: {id: live.id}}" class="card-body pb-1">
          <h5 class="card-title float-left mb-2">{{ live.title }}</h5>
          <h6 class="card-subtitle float-right small">Recorded : {{ displayDate(live.date) }}
          </h6>
          <p class="songdetail mb-2">
            <span v-for="sound in live.sounds" :key="'sound-' + sound.id">
              {{ sound.track_num }}. {{ sound.title }}
            </span>
          </p>
          <span class="p-0 pr-2 text-right small">ほか、全{{ live.sounds.length }}曲</span>
        </router-link>
      </article>
    </div>
  </section>
</div>
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
      if (error.message == 'Network Error' && error.response === undefined) {
        console.log('通信エラー');
      } else if (error.response.status === 500) {
        console.log('500')
      // } else if (error.response.status === 403){
      // } else if (error.response.status === 404){
      // } else {
      //   console.log(error.message);
      }
    })
    const displayDate = dateStr => moment(dateStr).format("YYYY/MM/DD (ddd)");
    const soundStaff = computed(() => store.state.user.is_staff);
    const secondToMMSS = seconds => {
      if (!(typeof seconds === "number")) {
        throw new Error("second must be a number")
      }
      const duration = moment.duration(seconds, "seconds");
      return `${duration.minutes}:${("00" + duration.seconds).slice(-2)}`
    }
    return {
      lives, soundStaff,
      displayDate, secondToMMSS
    }
  },
}
</script>

<style scoped>
article:hover{
  background-color: #e4f4f8;
}

.card-body{
  padding: 1rem;
}

h4.card-title{
  display: inline;
}

h6.card-subtitle{
  display: inline;
}

.card a{
  color: #212529;
}


a.card-body{
  text-decoration: none;
}

.songdetail{
  max-height: 48px;
  overflow: hidden;
}

.songdetail span{
  display: inline-block;
  white-space: nowrap;
}
</style>