<template>
  <div>
  <textarea
    name="content"
    v-model="content"
    cols="40"
    rows="10"
    placeholder="本文を入力"
    class="form-control"
    required="">
    </textarea>
  <validation-error-messages
    v-if="is_valid.length > 0 && isTouched"
    :messages="is_valid" />
  </div>
</template>

<script>
import validationErrorMessages from './send-validation-error.vue';
export default {
  data: () => ({
    isTouched: false
  }),
  components: {
    validationErrorMessages
  },
  computed: {
    content: {
      get() {
        return this.$store.state.send.content;
      },
      set(value) {
        this.isTouched = true;
        this.$store.commit('send/contentInput', value);
      }
    },
    is_valid() {
      return this.$store.getters['send/validateContent'];
    }
  }
}
</script>