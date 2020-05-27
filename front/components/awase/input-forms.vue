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
export default {
  props: {
    date: {type: String, required: true},// YYYYMMDD, String (example): '20200401']
    data: {type: Object, required: true},// extracted from app.timeScheduleData (example) {'20200401_0900': true, '20200401_0930': false}
    start: {type: Number, required: false, default: 9},
    end: {type: Number, required: false, default: 26},
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