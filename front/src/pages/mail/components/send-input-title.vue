<template>
  <div class="form-one-row">
    <label for="id_title">件名: </label>
    <input
      type="text"
      name="title"
      v-model="title"
      placeholder="件名を入力"
      class="pure-input-1"
      required
      id="id_title"
    />
    <ValidationErrorMessages
      v-if="error_messages.length > 0 && is_dirty"
      :messages="error_messages"
    />
  </div>
</template>

<script>
import ValidationErrorMessages from "../../../components/ValidationErrorMessages.vue";
import { computed } from "vue";
import { useStore } from "vuex";
export default {
  components: {
    ValidationErrorMessages,
  },
  setup() {
    const store = useStore();
    const title = computed({
      get: () => store.state.send.title["value"],
      set: (value) => store.commit("send/setTitle", value),
    });
    const is_dirty = computed(() => store.state.send.title["is_dirty"]);
    const error_messages = computed(
      () => store.state.send.title["error_messages"]
    );

    return {
      title,
      is_dirty,
      error_messages,
    };
  },
};
</script>