<template>
  <div class="form-one-row">
    <div class="pure-g">
      <div class="pure-u-1">
        <label for="year_choice">From:</label>
      </div>
      <div class="pure-u-1-3">
        <select
          name="year_choice"
          v-model="selectedYear"
          id="year_choice"
          class="pure-u-24-24"
        >
          <option v-for="year in years" :value="year" :key="year">
            {{ year }}
          </option>
        </select>
      </div>
      <div class="pure-u-2-3">
        <select
          name="member_choice"
          v-model="writer"
          class="pure-u-24-24"
          id="member_choice"
        >
          <option
            v-for="member in memberChoices"
            :value="member"
            :key="member.id"
          >
            {{ member.name }}
          </option>
        </select>
      </div>
    </div>
    <ValidationErrorMessages
      v-if="error_messages.length > 0 && is_dirty"
      :messages="error_messages"
    />
  </div>
</template>

<script>
import ValidationErrorMessages from "../../../components/ValidationErrorMessages.vue";
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import axios from "../../../utils/axios";
export default {
  components: {
    ValidationErrorMessages,
  },
  setup() {
    // vuexとの連携
    const store = useStore();
    const writer = computed({
      get: () => store.state.send.writer.value,
      set: (value) => store.commit("send/setWriter", value),
    });
    const is_dirty = computed(() => store.state.send.writer.is_dirty);
    const error_messages = computed(
      () => store.state.send.writer.error_messages
    );

    // コンポーネント内ディレクティブ
    const selectedYear = ref(store.state.mypage.userInfo.year);
    const years = ref([store.state.mypage.userInfo.year]);
    const members = ref([
      {
        year: store.state.mypage.userInfo.year,
        list: [
          {
            id: store.state.mypage.userInfo.id,
            name: store.state.mypage.userInfo.shortname,
            year: store.state.mypage.userInfo.year,
          },
        ],
      },
    ]);

    // craeted時、writerが設定されていなかったら自分を設定
    if (writer.value === null) {
      store.commit("send/setWriter", {
        id: store.state.mypage.userInfo.id,
        name: store.state.mypage.userInfo.shortname,
        year: store.state.mypage.userInfo.year,
      });
    }

    onMounted(() => {
      axios.get("/api/board/send/froms/").then((res) => {
        members.value = res.data.members;
        years.value = res.data.years;
      });
    });

    watch(selectedYear, (newSelectedYear) => {
      if (writer.value.year !== newSelectedYear) {
        store.commit("send/setWriter", null);
      }
    });

    // yearで絞り込むユーザーの選択肢
    const memberChoices = computed(() => {
      return members.value.find((obj) => {
        return obj.year === selectedYear.value;
      }).list;
    });

    return {
      writer,
      is_dirty,
      error_messages,
      selectedYear,
      years,
      memberChoices,
    };
  },
};
</script>

<style scoped>
/* .v-select-label {
  display: inline-block;
  width: 3rem;
}
#year_choice {
  display: inline-block;
  width: 5rem;
  padding: 6px;
}
#member_choice {
  display: inline-block;
  width: calc(100% - 9rem);
  min-width: 8rem;
  max-width: 18rem;
} */
</style>