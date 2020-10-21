<template>
  <div class="my-2">
    To: 
    <span class="selection">全回</span>
  </div>
</template>

<script>
export default {
  data: () => {
    return {
      years: [2020, 2019, 2018, 2017],
      selected: null
    }
  },
  methods: {
    yearToKi (year) {
      return year - 1994;
    }
  }
}
</script>

<style scoped>
.selection{
  padding: 6px;
  border-radius: 30%;
  font-size: 0.8rem;
  border: 1px solid #dddddd;
}
</style>