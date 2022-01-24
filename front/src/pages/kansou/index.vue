<template>
  <article>
    <h3>感想用紙</h3>
    <section v-for="year in yearsSet" :key="year" class="pure-menu-custom card">
      <h4 class="pure-menu-heading">{{ year }}年度</h4>
      <ul class="pure-menu-list">
        <li
          v-for="item in getItems(year)"
          :key="item.id"
          class="pure-menu-item kansou-item"
        >
          <a :href="`/download/kansou/${item.id}/`" target="_blank">
            {{ item.title }} ( {{ item.size }} )
          </a>
          <time :datetime="item.performedAt" class="small">
            {{ displayDate(item.performedAt) }}
          </time>
          <template v-if="item.detail">
            <br />
            <span class="small">
              {{ item.detail }}
            </span>
          </template>
        </li>
      </ul>
    </section>
  </article>
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

    axios
      .get("/api/kansou/")
      .then((res) => {
        kansou.length = 0;
        kansou.push(...res.data.kansou);
      })
      .catch((error) => {
        console.error(error.response);
        store.commit("message/addMessage", {
          level: "warning",
          message: "感想用紙のデータを取得できませんでした。",
          appname: "kansou/index",
        });
      });

    const years = computed(() =>
      kansou.map((item) => {
        const date = moment(item.performedAt);
        let year = 0;
        if (
          date.isBefore(moment().set({ year: date.year(), month: 3, day: 1 }))
        ) {
          year = date.year() - 1; //                       month:3 => 4月
        } else {
          year = date.year();
        }
        return year;
      })
    );
    const yearsSet = computed(() =>
      years.value.filter((x, i, self) => self.indexOf(x) === i).reverse()
    );
    // 重複しない年度の数字を取得

    const getItems = (year) => {
      return kansou
        .filter((item) =>
          moment(item.performedAt).isBetween(
            moment(`${year}-04-01`),
            moment(`${year + 1}-04-01`),
            undefined,
            "[)"
          )
        )
        .reverse();
    };

    const displayDate = (dateStr) => moment(dateStr).format("YYYY/MM/DD");
    const kansouStaff = computed(() => store.state.user.is_staff);

    return {
      yearsSet,
      kansouStaff,
      kansou,
      years,
      getItems,
      displayDate,
    };
  },
};
</script>

<style lang="scss" scoped>
.card {
  margin-bottom: 0.5rem;
}
.kansou-item {
  padding: 0.5em 1em;
  line-height: 1.5;
  time {
    padding: 0 0.5rem;
  }
}
</style>