<template>
  <div class="form-one-row">
    <div class="form-one-check">
      <span>[[hour]]:00</span>
      <button
        type="button"
        class="onetime false"
        :class="{'checked': isSelected_00 === false}"
        @click="onclick(0, false)"
        >×</button>
      <button
        type="button"
        class="onetime true"
        :class="{'checked': isSelected_00 === true}"
        @click="onclick(0, true)"
        >○</button>
    </div>
    <div class="form-one-check">
      <span>[[hour]]:30</span>
      <button
        type="button"
        class="onetime false"
        :class="{'checked': isSelected_30 === false}"
        @click="onclick(30, false)"
        >×</button>
      <button
        type="button"
        class="onetime true"
        :class="{'checked': isSelected_30 === true}"
        @click="onclick(30, true)"
        >○</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    hour: {type: Number, required: true},
    isSelected_00: {type: Boolean, required: false, default: null},
    isSelected_30: {type: Boolean, required: false, default: null}
  },
  methods: {
    onclick: function(minute, bool){
      this.$emit('time-click', {
        hour: this.hour,
        minute: minute,
        bool: bool
      });
      if (minute == 0){
      this.$emit('time-click', {
        hour: this.hour,
        minute: 30,//0分を押したときは30も発火
        bool: bool
      });
      }
    }
  }
}
</script>