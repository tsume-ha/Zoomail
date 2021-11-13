<template>
  <section>
    <h3>写真</h3>
    <p class="py-2">
      アンプラのイベントの写真を公開しています。<br>
      LiveLogに登録されていないBBQやお花見のイベントの写真もあります！
    </p>
    <div v-for="y in yearsSet" :key="y" class="row">
      <h4 class="col-12">{{y}}年度</h4>
      <div v-for="item in getItems(y)" :key="item.url" class="cardwrap col-6 col-xs-6 col-sm-6 col-md-4 col-lg-3 my-2">
        <article class="card">
          <img class="card-img-top" src="/static/img/album_thum_default.jpg" />
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
export default {
  setup() {
    const photos = reactive([
      {
        title: "ライブ1",
        date: "2021-01-01",
        url: "yahoo.co.jp"
      },
      {
        title: "ライブ2",
        date: "2021-05-01",
        url: "yahoo.co.jp"
      },
      {
        title: "ライブ3",
        date: "2021-06-01",
        url: "yahoo.co.jp"
      },
    ]);

    const years = computed(() => photos.map(item => {
      const date = moment(item.date);
      let year = 0;
      if (date.isBefore(moment().set({year:date.year(), month:3, day:1}))) {
        year = date.year() - 1;//                       month:3 => 4月
      } else {
        year = date.year()
      }
      return year;
    }));
    const yearsSet = computed(() => years.value.filter(
      (x, i, self) => self.indexOf(x) === i
    ).reverse());
    // 重複しない年度の数字を取得

    const getItems = year => {
      return photos.filter(item => moment(item.date).isBetween(
        moment().set({year:year, month:3, day:1}),
        moment().set({year:year+1, month:3, day:1},
        undefined, "[)")
      )).reverse();
    }

    const displayDate = dateStr => moment(dateStr).format("YYYY/MM/DD")

    return {
      photos, years, yearsSet,
      getItems, displayDate
    }
  },
}
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
</style>