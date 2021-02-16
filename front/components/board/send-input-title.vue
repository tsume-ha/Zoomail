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
    v-if="is_valid.length > 0 && isValidationDisplay"
    :messages="is_valid" />
</div>
</template>

<script>
import validationErrorMessages from './send-validation-error.vue';
export default {
  data: () => ({
    isTouched: false,
  }),
  components: {
    validationErrorMessages
  },
  computed: {
    title: {
      get () {
        return this.$store.state.send.title;
      },
      set (value) {
        this.isTouched = true;
        this.$store.commit('send/titleInput', value);
      }
    },
    is_valid () {
      return this.$store.getters['send/validateTitle'];
    },
    isValidationDisplay () {
      return this.$store.state.send.validate_clicked || this.isTouched;
    }
  }
}
</script>