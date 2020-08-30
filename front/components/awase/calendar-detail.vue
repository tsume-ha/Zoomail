<template>
  <div id="detail">
    <h5>{{date.format('MM/DD (ddd)')}}</h5>
    <h6>{{timeDisplay}}</h6>
    <span
      id="detail_close"
      @click="close"
      > </span>
    <ul v-if="hasData">
      <li v-for="data in scheduleDisplay" :key="data.name" class="row">
        <span class="col-8">{{data.name}}</span>
        <span class="col-4 text-center" :class="[boolToClassName(data.bool)]">{{boolToStr(data.bool)}}</span>
      </li>
    </ul>
    <div v-else class="text-center">集計範囲外です</div>
  </div>
</template>

<script>
import moment from "moment";
moment.locale('ja', {
  weekdays: ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日"],
  weekdaysShort: ["日", "月", "火", "水", "木", "金", "土"],
});
export default {
  props: {
    dataList: {required: true, type: Array},
    date: {required: true, type: Object},
    hour: {required: true, type: Number},
    minute: {required: true, type: Number},
  },
  computed: {
    timeDisplay: function () {
      let result = '';
      if (this.minute == 30) {
        result += String(this.hour) + ':' + '30';
        result += '～';
        result += String(this.hour + 1) + ':' + '00';
      } else {
        result += String(this.hour) + ':' + '00';
        result += '～';
        result += String(this.hour) + ':' + '30';
      }
      return result;
    },
    scheduleData () {
      return this.dataList.find(e => e['date'] == this.date.format('YYYY-MM-DD'));
    },
    hasData: function () {
      if (this.scheduleData === undefined) {
        return false;
      }
      if (this.scheduleData.hour_begin > this.hour) {
        return false;
      }
      if (this.scheduleData.hour_end <= this.hour) {
        return false;
      }
      return true;
    },
    scheduleDisplay () {
      if (this.scheduleData === undefined) {
        return [];
      }
      const keys = Object.keys(this.scheduleData.schedule_list);
      let result = [];
      const time = String(this.hour) + '_' + String(this.minute);
      for (const key of keys) {
        const data = this.scheduleData.schedule_list[key][time];
        result.push({name: key, bool: data});
      }
      return result;
    }
  },
  methods: {
    boolToStr: function (bool) {
      if (bool === undefined) {
        return '未回答';
      } else if (bool === false) {
        return '×';
      } else if (bool === true) {
        return '○';
      } else {
        // 例外処理
        console.log(bool);
        return String(bool);
      }
    },
    boolToClassName: function (bool) {
      if (bool === undefined) {
        return 'text-secondary';
      } else if (bool === false) {
        return 'text-danger';
      } else if (bool === true) {
        return 'text-success';
      } else {
        return '';
      }
    },
    close: function () {
      this.$emit('close-detail');
    }
  }
}
</script>

<style scoped>
div#detail{
  display: block;
  position: fixed;
  z-index: 10;
  background-color: rgba(255,255,255,0.8);
}


@media screen and (max-width: 767px) {/*767px以下*/
div#detail{
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  max-width: 500px;
  max-height: 50vh;
  margin: 0 auto;
  padding: 0 0;
  border-top: 1px dotted #999;
  overflow-y: scroll;
}
}
@media screen and (min-width: 768px) {/*768px以上*/
div#detail{
	width: 500px;
	margin: 1rem;
	padding: 0.5rem;
	top: 0;
	left: 0;
}
}

div#detail #detail_close{
	position: absolute;
	top: 0;
	right: 0;
	margin: 10px;
	padding: 12px;
	width: 24px;
	height: 24px;
	color: #F00;
	background-color: #fee;
  border-radius: 4px;
  border: 1px solid #faa;
}

div#detail #detail_close:before,
div#detail #detail_close:after{
  content: '';
  position: absolute;
  display: block;
  width: 16px;
  height: 1px;
  margin-left: -8px;
  background-color: currentColor;
}
div#detail #detail_close:before{
  -webkit-transform: rotate(45deg);
  transform: rotate(45deg);
}
div#detail #detail_close:after {
  -webkit-transform: rotate(-45deg);
  transform: rotate(-45deg);
}



div#detail h5,
div#detail h6{
    text-align: center;
}

div#detail ul{
    padding: 0;
    margin: 0;
    list-style: none;
}

div#detail ul li{
    margin: 0.25rem;
    padding: 0.25rem;
    border-bottom: 1px solid #aaa;
}
</style>