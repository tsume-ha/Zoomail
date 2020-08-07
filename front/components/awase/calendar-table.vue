<template>
    <div id="calendar-table">
      <calendar-leftside />
      <calendar-carousel />
    </div>
</template>

<script>
import calendarLeftside from './calendar-leftside.vue';
import calendarCarousel from './calendar-carousel.vue';
export default {
  components: {
    calendarLeftside,
    calendarCarousel
  },

}
</script>

<style scoped>
#calendar-table{
  display: flex;
  flex-direction: row;
  position: relative;
}
#calendar-table > div{
  position: relative;
  margin: 0;
  padding: 0;
}
#calendar-table > #calendar-leftside{
  display: inline-block;
  flex-basis: 40px;
  flex-shrink: 0;
  flex-grow: 0.25;
}
#calendar-table > #calendar-carousel{
  display: inline-block;
  flex-basis: auto;
  flex-shrink: 1;
  flex-grow: 10;
}
</style>