<template>
<div>
  <input
    type="text"
    name="title"
    v-model="title"
    placeholder="件名"
    class="form-control"
    required
    id="id_title" />
  <validation-error-messages
    v-if="error_messages.length > 0 && is_dirty"
    :messages="error_messages" />
</div>
</template>

<script>
import validationErrorMessages from '../../../components/validation-error-messages.vue';
import { computed } from 'vue';
import { useStore } from "vuex";
export default {
  components: {
    validationErrorMessages
  },
  setup() {
    const store = useStore();
    const title = computed({
      get: () => store.state.send.title["value"],
      set: value => store.commit('send/setTitle', value)
    });
    const is_dirty = computed(() => store.state.send.title["is_dirty"]);
    const error_messages = computed(() => store.state.send.title["error_messages"]);

    return {
      title, is_dirty, error_messages
    };
  }
};

</script>