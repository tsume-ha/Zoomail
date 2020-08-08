<template>
  <div class="calendar-column">
    {{date.format('YYYY-MM-DD')}}
  </div>
</template>

<script>
export default {
  props: {
    // columndata: {required: false, type: Object},
    date: {required: true, type: Object}
  },
  data: function () {
    return {
      // date: '2020-08-01'
    }
  },

}
</script>