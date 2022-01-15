<template>
  <article>
    <h3>写真</h3>
    <p>
      アンプラのイベントの写真を公開しています。<br />
      LiveLogに登録されていないBBQやお花見のイベントの写真もあります!
    </p>
    <div class="pure-g">
      <div
        v-for="photo in photos"
        :key="'photo-' + photo.id"
        class="
          pure-u-1-2 pure-u-sm-1-3 pure-u-md-1-4 pure-u-lg-1-5
          card-wrapper
        "
      >
        <a :href="photo.url" class="card-photo" target="_blank">
          <img
            v-if="photo.thumbnail"
            :src="photo.thumbnail"
            :alt="`${photo.title} - サムネイル`"
            class="pure-img"
          />
          <img
            v-else
            src="@/assets/img/unplugged_logo.jpg"
            :alt="`${photo.title} - サムネイル`"
            class="pure-img"
          />
          <span class="photo-title">{{ photo.title }}</span>
          <span class="photo-date">{{ displayDate(photo.date) }}</span>
        </a>
      </div>
    </div>
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
    const photos = reactive([]);

    axios
      .get("/api/photo/")
      .then((res) => {
        photos.length = 0;
        photos.push(...res.data.photos);
      })
      .catch((error) => {
        console.error(error.response);
        store.commit("message/addMessage", {
          level: "warning",
          message: "アルバムを取得できませんでした。",
          appname: "photos/index",
        });
      });

    const years = computed(() =>
      photos.map((item) => {
        const date = moment(item.date);
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
      return photos
        .filter((item) =>
          moment(item.date).isBetween(
            moment(`${year}-04-01`),
            moment(`${year + 1}-04-01`),
            undefined,
            "[)"
          )
        )
        .reverse();
    };

    const displayDate = (dateStr) => moment(dateStr).format("YYYY/MM/DD");
    const thumbnailPath = (item) => {
      if (item.thumbnail) {
        return item.thumbnail;
      } else {
        return "/static/img/album_thum_default.jpg";
      }
    };

    const photoStaff = computed(() => store.state.user.is_staff);

    return {
      photos,
      years,
      yearsSet,
      photoStaff,
      getItems,
      displayDate,
      thumbnailPath,
    };
  },
};
</script>

<style lang="scss" scoped>
.card-wrapper {
  padding: 1rem 0.5rem;

  .card-photo {
    display: inline-block;
    position: relative;
    border-radius: 3px;
    color: #fff;
    transition: 0.4s;

    &:hover {
      text-decoration: none;
      color: #000;
      &::after {
        background-color: rgba(255, 255, 255, 1);
        box-shadow: inset 0 0 0px 5px rgba(0, 0, 0, 0.8);
      }
    }
    &::after {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border-radius: 3px;
      background-color: rgba(0, 0, 0, 0.8);
      box-shadow: inset 0 0 0px 5px rgba(255, 255, 255, 1);
      opacity: 0.3;
      transition: background-color 0.4s;
      z-index: 1;
    }

    img {
      position: relative;
      border-radius: 3px;
    }
    .photo-title,
    .photo-date {
      position: absolute;
      z-index: 2;
      max-width: calc(100% - 10px - 1.5rem);
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .photo-title {
      top: 0.75rem;
      left: 0.75rem;
    }
    .photo-date {
      bottom: 0.75rem;
      right: 0.75rem;
      font-size: 0.75rem;
    }
  }
}
</style>