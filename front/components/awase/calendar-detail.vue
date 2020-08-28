<template>
  <div id="detail">
    <span v-on:click="detail_close" id="detail_close"></span>
    <h5>{{date.format('MM/DD（ddd）')}}</h5>
    <h6>{{timeDisplay}}</h6>
    <ul>
    
    </ul>
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
    isActive: {required: true, type: Boolean},
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
      let data = this.dataList.find(e => e['date'] == this.date.format('YYYY-MM-DD'));
      return data.schedule_list;
    },
    scheduleDisplay () {
      const keys = Object.keys(this.scheduleData);
      let result = [];
      const time = String(this.hour) + '_' + String(this.minute);
      for (const key of keys) {
        const data = this.scheduleData[key][time];
        result.push({[key]: data});
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
      }
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
  top: 0;
  left: 100px;
}

#calendar_detail{
	display: none;
}

#calendar_detail.opened{
    display: block;
    position: fixed;
    z-index: 10;
    background-color: rgba(255,255,255,0.8);
}

@media screen and (max-width: 767px) {/*767px以下*/
#calendar_detail.opened{
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
#calendar_detail.opened{
	width: 500px;
	margin: 1rem;
	padding: 0.5rem;
	top: 0;
	left: 0;
}
}

#calendar_detail.opened #detail_close{
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

#calendar_detail.opened #detail_close:before,
#calendar_detail.opened #detail_close:after{
    content: '';
    position: absolute;
    display: block;
    width: 16px;
    height: 1px;
    margin-left: -8px;
    background-color: currentColor;
}
#calendar_detail.opened #detail_close:before{
    -webkit-transform: rotate(45deg);
    transform: rotate(45deg);
}
#calendar_detail.opened #detail_close:after {
    -webkit-transform: rotate(-45deg);
    transform: rotate(-45deg);
}



#calendar_detail.opened h5,
#calendar_detail.opened h6{
    text-align: center;
}

#calendar_detail.opened ul{
    padding: 0;
    margin: 0;
    list-style: none;
}

#calendar_detail.opened ul li{
    margin: 0.25rem;
    padding: 0.25rem;
    border-bottom: 1px solid #aaa;
}
</style>