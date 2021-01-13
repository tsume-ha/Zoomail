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
    <ul v-if="is_valid.length > 0 && isTouched">
      <li v-for="message in is_valid" :key="message" v-text="message"></li>
    </ul>
  </div>
</template>

<script>
export default {
  data: () => ({
    isTouched: false
  }),
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