<template>
  <div id="calendar-leftside">
    <div class="date"></div>
    <div class="room">
      例会
    </div>
    <template v-for="h in (displayTimeRange.end - displayTimeRange.begin)">
      <div class="time" :class="(h+displayTimeRange.begin+-1)+'00'" :key="(h+displayTimeRange.begin+-1)+'00'">
        {{h+displayTimeRange.begin+-1}}:00
      </div>
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
@import "./calendar-table-cell.css";
#calendar-leftside{
  border-left: 1px solid #eee;
  border-right: 1px solid #eee;
}
.time{
  font-size: 10px;
  padding: 0 5px;
}
.time:nth-child(2n){
  border-top: none;
}
</style>
