<template>
  <div>test</div>
</template>

<script>
export default {
  name: 'index',
  computed: {
    test () {
      return this.$store.state.read.test;
    }
  }
}
</script>