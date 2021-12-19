<template>
  <ul>
    <li
      v-for="message in messages"
      :key="message"
      v-text="message"
      class="text-danger small my-1"
    ></li>
  </ul>
</template>

<script>
export default {
  name: "validation-error-messages",
  props: {
    messages: { required: true, type: Array },
  },
};
</script>

<style lang="scss" scoped>
ul {
  list-style: none;
  margin: 5px 0 0 1rem;
  padding: 0;
  color: $text-red;

  li {
    background-color: $bg-white;
    display: inline-block;
    padding: 0.25rem;
    margin: 0 0 1px 0;
    border-radius: 4px;
    background-color: $bg-red;
  }
}
</style>