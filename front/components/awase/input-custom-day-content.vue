<template>
  <div
    class="ceil text-center pt-1 pb-2"
    @click="onclick"
    :class="{active: isActive, selected: isSelected}"
  >
    <h6 class="m-0 p-0" :style="addStyleTextColor(day.weekday)">{{day.day}}</h6>
    <span class="small">{{displayHour}}</span>
  </div>
</template>

<script>
export default {
  props: {
    day: {type: Object, required: true},
    data: {type: Object, required: false, default: () => {return{start: '', end: ''}},},
    isSelected: {type: Boolean, required: false}
  },
  methods: {
    onclick: function(){
      this.$emit('dayselected', this.day);
    },
    addStyleTextColor: function(weekday) {
      if (weekday === 1) {
        return {
          color: "red"
        };
      } else if (weekday === 7) {
        return {
          color: "#1669a8"
        };
      }
    }
  },
  computed: {
    displayHour: function(){
      let start = this.data.start;
      let end = this.data.end;
      if (!this.isActive) {
        return '-';
      } else if (start === end) {
        return '×';
      } else {
        return start + '-' + end;
      }
    },
    isActive: function(){
      return !(this.data.start === '' && this.data.end === '');
    }
  }
};
</script>
<style scoped>
/* Calendar内のcss */
.ceil{
    cursor: default;
}
.ceil.active{
    cursor: pointer;
}
.ceil.selected{
    background-color: #adddeb;
}
</style>