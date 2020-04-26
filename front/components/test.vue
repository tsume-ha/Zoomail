<template>
  <div>
    <p v-if="isVisible">{{ message }}</p>
  </div>
</template>
<script>
module.exports = {
  name: "test",
  data: function() {
    return {
      message: "hello world!",
    };
  },
  computed: {
    isVisible: function() {
      if (this.message) {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>
<style scoped></style>