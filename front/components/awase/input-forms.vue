<template>
  <div class="form-group">
    <div class="form-oneday-all">
      <span class="mx-3">１日一括指定</span>
      <button
        type="button"
        class="dayall false"
        @click="onAlldayClicked(false)">×</button>
      <button
        type="button"
        class="dayall true"
        @click="onAlldayClicked(true)">○</button>
    </div>
    <input-one-row
      v-for="t in timeRange"
      :key="t + start - 1"
      :hour="t + start - 1"
      :isSelected_00="getScheduleBool((t + start - 1), 0)"
      :isSelected_30="getScheduleBool((t + start - 1), 30)"
      @time-click="onOneRowClicked"
      >
    </input-one-row>
  </div>
</template>

<script>
import oneRow from './input-one-row.vue';
export default {
  props: {
    date: {type: String, required: true},// YYYYMMDD, String (example): '20200401']
    data: {type: Object, required: true},// extracted from app.timeScheduleData (example) {'20200401_0900': true, '20200401_0930': false}
    start: {type: Number, required: false, default: 9},
    end: {type: Number, required: false, default: 26},
  },
  components: {
    "input-one-row": oneRow,
  },
  methods: {
    onOneRowClicked: function(e){
      // e: Object, (example) {hour: 12, minute: 0, bool: true}
      this.$emit('value-change', e);
    },
    onAlldayClicked: function(bool){
      for (let hour = this.start; hour < this.end; hour++) {
        for (let minute of [0, 30]) {
          this.$emit('value-change', {
            hour: hour,
            minute: minute,
            bool: bool
          });
        }
      }
    },
    getScheduleBool: function (hour, minute) {
      let key = this.date + '_' + ('0' + hour).slice(-2) + ('0' + minute).slice(-2);
      return this.data[key];
    }
  },
  computed: {
    timeRange: function(){
      return this.end - this.start;
    },
  }
};
</script>

<style scoped>
/* inputのcss */
#input-form{
  z-index: 5;
}
#input-form h5{
  margin: 16px 0 8px 4rem;
  height: 24px;
  line-height: 24px;
}
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
.form-group button{
  background-color: rgba(255, 255, 255, 0);
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