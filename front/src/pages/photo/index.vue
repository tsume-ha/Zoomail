<template>
  <section>
    <h3>写真</h3>
    <p class="py-2">
      アンプラのイベントの写真を公開しています。<br>
      LiveLogに登録されていないBBQやお花見のイベントの写真もあります！
    </p>
    <div class="row" v-if="photoStaff" v-cloak>
      <a href="/admin/pictures/album/">アルバムの登録・編集はこちらから</a>
    </div>
    <div v-for="y in yearsSet" :key="y" class="row">
      <h4 class="col-12">{{y}}年度</h4>
      <div v-for="item in getItems(y)" :key="item.id" class="cardwrap col-6 col-xs-6 col-sm-6 col-md-4 col-lg-3 my-2">
        <article class="card">
          <img class="card-img-top" :src="thumbnailPath(item)" />
          <a :href="item.url" class="card-img-overlay" target="_blank">
            <h5 class="card-title" v-text="item.title"></h5>
            <span>{{ displayDate(item.date) }}</span>
          </a>
        </article>
      </div>
    </div>
  </section>
</template>

<script>
import moment from "../../utils/moment";
import { computed, reactive } from "vue";
import axios from "../../utils/axios";
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const photos = reactive([]);

    axios.get("/api/photo/").then(res => {
      photos.length = 0;
      photos.push(...res.data.photos);
    }).catch(error => {
      console.error(error.response);
      store.commit('message/addMessage', {
        level: "warning",
        message: "アルバムを取得できませんでした。",
        appname: "photos/index"
      });
    });

    const years = computed(() => photos.map(item => {
      const date = moment(item.date);
      let year = 0;
      if (date.isBefore(moment().set({year:date.year(), month:3, day:1}))) {
        year = date.year() - 1;//                       month:3 => 4月
      } else {
        year = date.year();
      }
      return year;
    }));
    const yearsSet = computed(() => years.value.filter(
      (x, i, self) => self.indexOf(x) === i
    ).reverse());
    // 重複しない年度の数字を取得

    const getItems = year => {
      return photos.filter(item => moment(item.date).isBetween(
        moment(`${year}-04-01`),
        moment(`${year+1}-04-01`),
        undefined, "[)")
      ).reverse();
    };

    

    const displayDate = dateStr => moment(dateStr).format("YYYY/MM/DD");
    const thumbnailPath = item => {
      if (item.thumbnail) {
        return item.thumbnail;
      } else {
        return "/static/img/album_thum_default.jpg";
      }
    };

    const photoStaff = computed(() => store.state.user.is_staff);

    return {
      photos, years, yearsSet, photoStaff,
      getItems, displayDate, thumbnailPath
    };
  },
};
</script>

<style scoped>
a.card-img-overlay{
  border-radius: 3px;
  color: #fff;
  background-color: rgba(0,0,0,0.3);
  transition: 0.4s;
}

a.card-img-overlay:after{
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 3px;
  box-shadow: inset 0 0 0px 5px rgba(255,255,255,0.5);
}

a.card-img-overlay.hover{
  text-decoration: none;
  color: #000;
  background-color: rgba(255,255,255,0.5);
}

h6.card-subtitle{
  position: absolute;
  right: 1rem;
  bottom: 1rem;
  font-size: 0.75rem;
  font-weight: 400;
  color: #fff;
  transition: 0.4s;
}
a.card-img-overlay.hover h6.card-subtitle{
  color: #000;
  text-decoration: none;
}
[v-cloak] {
  display: none;
}
</style>