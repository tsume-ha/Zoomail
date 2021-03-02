<template>
  <div
    class="ceil text-center pt-1 pb-2"
    @click="onclick"
    :class="{selected: isSelected}"
  >
    <h6 class="m-0 p-0" :style="addStyleTextColor(day.weekday)">{{day.day}}</h6>
    <span class="room-detail">{{room}}</span>
  </div>
</template>

<script>
export default {
  props: {
    day: {type: Object, required: true},
    data: {type: Object, required: false, default: () => ({"room": null})},
    isSelected: {type: Boolean, required: false}
  },
  methods: {
    onclick: function(){
      if (this.isSelected) {
        this.$emit('dayremove', this.day);
      } else {
        this.$emit('dayadd', this.day);
      }
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
    room () {
      if (this.data.room == null) {
        return '-';
      }
      else {
        return this.data.room
      }
    }
  }
};
</script>
<style scoped>
/* Calendar内のcss */
.ceil{
  cursor: pointer;
}
.ceil.selected{
  background-color: #adddeb;
}
.ceil .room-detail{
  font-size: 0.5rem;
  
}
</style>