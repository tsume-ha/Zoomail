<template>
  <div class="form-one-row">
    <div class="v-select-label">To:</div>
    <div class="v-select-wraper">
      <VSelect v-model="tos" :options="years" label="label" multiple />
    </div>
  </div>
  <ValidationErrorMessages
    v-if="error_messages.length > 0 && is_dirty"
    :messages="error_messages"
  />
</template>

<script>
import ValidationErrorMessages from "../../../components/ValidationErrorMessages.vue";
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import axios from "../../../utils/axios";
import VSelect from "vue-select";
import "vue-select/dist/vue-select.css";
export default {
  components: {
    ValidationErrorMessages,
    VSelect,
  },
  setup() {
    const store = useStore();
    const tos = computed({
      get: () => store.state.send.tos["value"],
      set: (value) => store.commit("send/setTos", value),
    });
    const is_dirty = computed(() => store.state.send.tos["is_dirty"]);
    const error_messages = computed(
      () => store.state.send.tos["error_messages"]
    );

    const toGrouplabel = (year) => `${String(year)} ${String(year - 1994)}期`;
    const userYear = store.state.user.year;
    // 選択肢
    const years = ref([
      {
        year: 0,
        label: "全回メーリス",
      },
      {
        year: userYear,
        label: toGrouplabel(userYear),
      },
    ]);
    onMounted(() => {
      axios.get("/api/board/send/togroups/").then((res) => {
        years.value.length = 0;
        res.data.togropus.forEach((y) => {
          years.value.push(y);
        });
      });
    });
    return {
      tos,
      is_dirty,
      error_messages,
      years,
    };
  },
};
</script>

<style lang="scss">
.v-select-wraper {
  background-color: $bg-white;
  border-radius: 4px;
}
</style>