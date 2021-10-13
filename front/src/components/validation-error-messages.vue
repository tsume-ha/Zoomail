<template>
  <ul>
    <li
      v-for="message in messages"
      :key="message"
      v-text="message"
      class="text-danger small my-1"></li>
  </ul>
</template>

<script>
export default {
  name: "validation-error-messages",
  props: {
    messages: {required: true, type: Array}
  }
}
</script>

<style scoped>
ul{
  list-style: none;
  margin: 5px 0 0 1rem;
  padding: 0;
}
</style>