<template>
  <div class="row row-wraper" :class="{notselected: notselected}">
    <div
      class="date col-3"
      :class="date | dayColor"
      @click="onclicked">
      {{date | md}}<wbr>
      ({{date | youbi}})
    </div>
    <div
      class="input col-9">
      <input
        type="text"
        v-model="room"
        autocomplete="on"
        list="room-choices"
        class="form-control"
        :class="{queued}">
    </div>
  </div>
</template>

<script>
import moment from 'moment/moment'
moment.locale('ja')
export default {
  props: {
    data: {type: Object, required: true, default: {"date": null, "room": null}},
    notselected: {type: Boolean, required: false, default: false},
    queued: {type: Boolean, required: false, default: false}
  },
  computed: {
    date () {
      if (this.data['date']==null){
        return null
      }
      return moment(this.data['date']);
    },
    room: {
      get () {
        if (!this.data.room) {
            return '';
          }
        return this.data.room;
      },
      set (value) {
        this.$emit('oninput', {"room": value, "date": this.date.format('YYYY-MM-DD')});
      }
    }
  },
  methods: {
    onclicked () {
      this.$emit('dayclicked', this.date);
    },
  },
  filters: {
    md (date) {
      return date.format('MM/DD')
    },
    youbi (date) {
      return date.format('dd')
    },
    dayColor(date) {
      let day = date.format('d')
      switch (day) {
        case '0':
          return 'text-danger';
        case '6':
          return 'text-primary';
        default:
          return '';
      }
    },
  }
}
</script>

<style scoped>
.row-wraper{
  border-top: 1px solid #ddd;
}
.row-wraper.notselected{
  background-color: #ddd;
}
.date{
  display: inline-block;
  font-size: 0.75rem;
  text-align: center;
  padding-top: 0.5rem;
}
input.queued{
  box-shadow: 0 0 2px 2px #28a745 inset;
}
</style>