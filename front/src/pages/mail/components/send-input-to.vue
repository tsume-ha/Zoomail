<template>
  <div>
    <div class="my-2">
      <div class="v-select-label">
      To: 
      </div>
      <div class="v-select-wraper">
        <v-select
          v-model="tos"
          :options="years"
          label="label"
          :reduce="obj => obj.year"
          multiple
        >
        </v-select>
      </div>
    </div>
    <validation-error-messages
      v-if="error_messages.length > 0 && is_dirty"
      :messages="error_messages" />
  </div>
</template>

<script>
import validationErrorMessages from '../../../components/validation-error-messages.vue';
import { computed, onMounted, ref } from 'vue';
import { useStore } from "vuex";
import axios from '../../../utils/axios';
import vSelect from 'vue-select';
import 'vue-select/dist/vue-select.css';
export default {
  components: {
    validationErrorMessages,
    vSelect
  },
  setup() {
    const store = useStore();
    const tos = computed({
      get: () => store.state.send.tos["value"],
      set: value => store.commit('send/setTos', value)
    });
    const is_dirty = computed(() => store.state.send.tos["is_dirty"])
    const error_messages = computed(() => store.state.send.tos["error_messages"])

    const toGrouplabel = year => String(year) + " " + String(year - 1994) + "期"
    const userYear = store.state.user.year
    // 選択肢
    const years = ref([
      {
        year: 0,
        label: "全回メーリス"
      },
      {
        year: userYear,
        label: toGrouplabel(userYear)
      }
    ])
    onMounted(() => {
      axios.get("/api/board/send/togroups/").then(res => {
        years.value = res.data.togropus
      })
    })
    return {
      tos, is_dirty, error_messages, years
    }
  }
}
</script>

<style scoped>
.v-select-label{
  display: inline-block;
  width: 3rem;
}
.v-select-wraper{
  display: inline-block;
  width: calc(100% - 4rem);
}
</style>