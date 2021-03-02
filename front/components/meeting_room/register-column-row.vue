<template>
  <div>
    <span class="is-selected">
      {{selected}}
    </span>
    <span class="date">
      {{date | md}}
    </span>
    <input type="text" :value="room" autocomplete="on" list="room-choices">
  </div>
</template>

<script>
import moment from 'moment/moment'
moment.locale('ja')
export default {
  props: {
    data: {type: Object, required: true, default: {"date": null, "room": null}},
    selected: {type: Boolean, required: false, default: false}
  },
  data: () => ({
    room: "",
    choices: [
      '4共21',
      '4共22',
      '4共30',
      '終日使用不可'
    ]
  }),
  mounted () {
    if (!this.data.room) {
        this.room = '未登録';
      }
    this.room = this.data.room;
  },
  computed: {
    date () {
      if (this.data['date']==null){
        return null
      }
      return moment(this.data['date']);
    }
  },
  filters: {
    md (date) {
      return date.format('MM/DD (dd)')
    }
  }
}
</script>