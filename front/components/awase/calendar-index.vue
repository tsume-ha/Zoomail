<template>
<div>
  <section id="calendar">
  <awase-calendar />
  </section>

  <section id="menu" class="col-xs-12 col-sm-8 col-md-6 col-ld-6 my-4">
    <awase-calendar-menu />
  </section>

  <section id="exapmle">
    <awase-calendar-example />
  </section>
</div>
</template>

<script>
import awaseCalendar from "./calendar.vue";
import awaseCalendarMenu from "./calendar-menu.vue";
import awaseCalendarExample from "./calendar-example.vue";
export default {
  components: {
    awaseCalendar,
    awaseCalendarMenu,
    awaseCalendarExample
  },
}
</script>