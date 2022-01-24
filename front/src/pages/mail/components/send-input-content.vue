<template>
  <div class="form-one-row">
    <label for="id_content">本文: </label>
    <textarea
      name="content"
      v-model="content"
      cols="40"
      rows="10"
      placeholder="本文を入力"
      class="pure-input-1"
      id="id_content"
      required=""
    >
    </textarea>
    <ValidationErrorMessages
      v-if="error_messages.length > 0 && is_dirty"
      :messages="error_messages"
    />
  </div>
</template>s

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
    const content = computed({
      get: () => store.state.send.content["value"],
      set: (value) => store.commit("send/setContent", value),
    });
    const is_dirty = computed(() => store.state.send.content["is_dirty"]);
    const error_messages = computed(
      () => store.state.send.content["error_messages"]
    );

    return {
      content,
      is_dirty,
      error_messages,
    };
  },
};
</script>