<template>
<div>
  <input
    type="text"
    name="title"
    v-model="title"
    @change="isTouched=true"
    placeholder="件名"
    class="form-control"
    required
    id="id_title" />
  <ul v-if="is_valid.length > 0 && isTouched">
    <li v-for="message in is_valid" :key="message" v-text="message"></li>
  </ul>
</div>
</template>

<script>
export default {
  data: () => ({
    isTouched: false,
  }),
  computed: {
    title: {
      get () {
        return this.$store.state.send.title;
      },
      set (value) {
        this.$store.commit('send/titleInput', value);
      }
    },
    is_valid () {
      return this.$store.getters['send/validateTitle'];
    }
  }
}
</script>