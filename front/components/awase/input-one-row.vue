<template>
  <div class="form-one-row">
    <div class="form-one-check">
      <span>{{hour}}:00</span>
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
      <span>{{hour}}:30</span>
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

<style scoped>
/* inputのcss */
.form-group *{
  letter-spacing:normal;
}
.form-one-check,
.form-oneday-all{
  display: inline-block;
  padding: 0.25rem 0;
  margin: 0;
  width: 50%;
  height: 42px;
  border: none;
  box-sizing: inherit;
}
.form-one-row:nth-of-type(2n+1){
  background-color: #f3f3f3;
}
.form-oneday-all{
  width: 100%;
  background-color: #ffffcc;
  border-top: 1px solid #abcdef;
  border-bottom: 1px solid #abcdef;
  padding: 0.5rem 0;
  height: auto;
}
.form-one-check span{
  display: inline-block;
  width: 2.5rem;
  margin: 0 4px 0 8px;
  padding: 0;
}
.form-one-row{
  display: flex;
}
.dayall,
.onetime{
  display: inline-block;
  position: relative;
  width: 24%;
  max-width: 5rem;
  text-align: center;
  padding: 0rem;
  margin: 0;
  border-radius: 0.6rem;
  font-size: 1.4rem;
  line-height: 2rem;
  background: transparent;
  }
.dayall.true,
.onetime.true{
  border: 1px solid transparent;
  color: #4cd964;
}
.dayall.true,
.onetime.true.checked{
  background-color: #4cd964;
  color: #fff;
}

.dayall.false,
.onetime.false{
  border: 1px solid transparent;
  color: #ff3b30;
}
.dayall.false,
.onetime.false.checked{
  background-color: #ff3b30;
  color: #fff;
}

</style>