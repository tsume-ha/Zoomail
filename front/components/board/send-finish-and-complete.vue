<template>
  <div>send-finish-and-complete

    {{progress}}%
  </div>
</template>

<script>
export default {
  computed: {
    progress () {
      return this.$store.state.send.progress;
    }
  }
}
</script>