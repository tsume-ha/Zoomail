<template>
  <div id="calendar-leftside">
    <div class="date"></div>
    <div class="room">
      例会
    </div>
    <template v-for="h in (displayTimeRange.end - displayTimeRange.begin)">
      <div class="time" :class="(h+displayTimeRange.begin+-1)+'00'" :key="(h+displayTimeRange.begin+-1)+'00'"></div>
      <div class="time" :class="(h+displayTimeRange.begin+-1)+'30'" :key="(h+displayTimeRange.begin+-1)+'30'"></div>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    displayTimeRange: {required: false, type: Object, default: () => {return {begin:9, end:21}}}
  },
    
}
</script>

<style scoped>
.room{
  font-size: 10px;
  text-align: center;
  padding: 5px 0;
  line-height: 15px;
  height: 26px;
  word-break: break-all;
  overflow-x: hidden;
  overflow-y: hidden;
  z-index: 2;
}
</style>
