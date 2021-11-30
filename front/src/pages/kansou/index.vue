<template>
  <main>
    <section v-for="year in yearsSet" :key="year">
      <h4>{{year}}年度</h4>
      <p v-for="item in getItems(year)" :key="item.id">
        <a :href="item.url" target="_blank">{{item.title}}</a><br>
        {{item.performedAt}}

      </p>
    </section>

  </main>
</template>

<script>
import moment from "../../utils/moment";
import { computed, reactive } from "vue";
import axios from "../../utils/axios";
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const kansou = reactive([]);

    axios.get("/api/kansou/").then(res => {
      kansou.length = 0;
      kansou.push(...res.data.kansou);
    }).catch(error => {
      console.error(error.response);
      store.commit('message/addMessage', {
        level: "warning",
        message: "感想用紙のデータを取得できませんでした。",
        appname: "kansou/index"
      });
    });

    const years = computed(() => kansou.map(item => {
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
      return kansou.filter(item => moment(item.date).isBetween(
        moment(`${year}-04-01`),
        moment(`${year+1}-04-01`),
        undefined, "[)")
      ).reverse();
    };

    

    const displayDate = dateStr => moment(dateStr).format("YYYY/MM/DD");
    const kansouStaff = computed(() => store.state.user.is_staff);

    return {
      yearsSet, kansouStaff,
      getItems, displayDate
    };

  },
};
</script>