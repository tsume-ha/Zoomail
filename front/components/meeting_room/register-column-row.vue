<template>
  <div class="row row-wraper" :class="{selected: selected}">
    <div
      class="date col-3"
      @click="onclicked">
      {{date | md}}<!--  <br> -->
      ({{date | youbi}})
    </div>
    <div
      class="input col-9">
      <input
        type="text"
        v-model="room"
        autocomplete="on"
        list="room-choices">
    </div>
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
  // data: () => ({
  //   // room: "",
  //   choices: [
  //     '4共21',
  //     '4共22',
  //     '4共30',
  //     '終日使用不可'
  //   ]
  // }),
  // mounted () {
  //   if (!this.data.room) {
  //       this.room = '未登録';
  //     }
  //   this.room = this.data.room;
  // },
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
      if (this.selected) {
        this.$emit('dayremove', this.date);
      } else {
        this.$emit('dayadd', this.date);
      }
    },
    // oninput () {
    //   this.$emit('input', {"str": this.})
    // }
  },
  filters: {
    md (date) {
      return date.format('MM/DD')
    },
    youbi (date) {
      return date.format('dd')
    }
  }
}
</script>

<style scoped>
.row-wraper{
  border-top: 1px solid #ddd;
}
.row-wraper.selected{
  background-color: #ddd;
}
.date{
  display: inline-block;
  font-size: 0.75rem;
  text-align: center;
}
</style>