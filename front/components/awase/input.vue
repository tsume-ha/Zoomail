<template>
  <section class="input-wrap row mt-3 border-top" @click="isMenuOpen = false">
    <template v-if="jsonLoaded">
    <nav id="input-nav" @click.stop="isMenuOpen = true" :class="{'active': isMenuOpen}" class="pt-3">
      <div id="calendar-wrap">
        <h5 class="px-3">日付を選択</h5>
        <v-calendar
        :first-day-of-week="2"
        is-expanded
        >
          <template slot='header-title' slot-scope='props'>
            {{props.yearLabel}}年{{props.monthLabel}}
          </template>
          <template slot='day-content' slot-scope='props'>
            <custom-day-content
              :day="props.day"
              :data="timeRangeData[dateToYYYYMMDD(props.day.date)]"
              :is-selected="dateToYYYYMMDD(props.day.date) == selectedDate"
              @dayselected="daySelected"
              ></custom-day-content>
          </template>
        </v-calendar>
      </div>
    </nav>
    <button type="button" @click.stop="isMenuOpen = !isMenuOpen" id="menu-switch" :class="{'active': isMenuOpen}">
      <img src="/static/img/calendar-menu.png" width="32" height="32" alt="Open Date Picker" />
    </button>
    <form id="input-form" class="pt-3">
      <h5 :class="{'active': isMenuOpen}">{{YYYYMMDDToTitle}}</h5>
      <div class="d-inline-block my-2">
        <button type="button" @click="moveDay(-1)" class="btn btn-info mx-1">前の日に</button>
        <button type="button" @click="moveDay(1)" class="btn btn-info">次の日に</button>
      </div>
      <input-forms
        v-if="isActiveDay"
        :date="selectedDate"
        :data="selectedDateScheduleData"
        :start="timeRangeData[selectedDate].start"
        :end="timeRangeData[selectedDate].end"
        @value-change="onValueChange"></input-forms>
      <p v-else>
        この日にちの集計はおこなわれていません。
      </p>
      <p v-if="isProcessError" v-text="errorMessage" class="text-danger"></p>
      <button type="button" v-if="isProcessError" @click="POST" class="btn btn-danger m-3">再送信</button>
      <p v-if="whenPageLeave" class="text-info">バックグラウンドで通信中です。通信が終わるまで、このページを開いたままにしてください！</p>
      <p v-text="afterErrorMessage" class="text-success"></p>
      <p class="small mx-2">
        サーバーとの通信が自動で行われるようになり、送信ボタンが無くなりました。
      </p>
      <a href="../" class="btn btn-secondary m-2">戻る</a>
    </form>
    <div v-if="isInAccess" class="small text-secondary is-in-access">サーバーと通信中...</div>
    </template>
    <p v-else>
      Loading...
    </p>
  </section>

</template>

<script>
import customDayContent from './input-custom-day-content.vue';
import forms from './input-forms.vue';
import Calendar from 'v-calendar/lib/components/calendar.umd'

export default {
  props: {
    jsonUrl: {type: String, required: true}
  },
  components: {
    "custom-day-content": customDayContent,
    "input-forms": forms,
    "v-calendar": Calendar,
  },
  data: function() {
    return {
      isMenuOpen: true,
      jsonLoaded: false,
      isProcessError: false,
      errorMessage: '',// String, (example) '404エラーです'
      afterErrorMessage: '',//String エラーが回復したときのメッセージ
      isInAccess: false,
      whenPageLeave: false,
      timeRangeData: {},//Object, (example) {'20200401': {start: 9, end: 26},}
      timeScheduleData: {},//Object (example) {'20200403_0900': false, '20200403_2030': true}
      selectedDate: '',//YYYYMMDD, String  (example) '20200401'
      beforePOSTRequest: {},// timeScheduleDataとおなじ形式
    }
  },
  created: function(){
    this.axios
      .get(this.jsonUrl)
      .then((res) => {
        console.log(res);
        this.timeRangeData = res.data.HourRange;
        this.timeScheduleData = res.data.Schedule;
        this.selectedDate = res.data.InitialDate;

        this.jsonLoaded = true;
      });
  },
  mounted: function(){
    $(window)
      .off('beforeunload')
      .on('beforeunload', () => {
        if (this.isInAccess){
          this.whenPageLeave = true;
          return 'バックグラウンドでデータを転送中です！終了するまで、このページを開いたままにしてください！';
        }
      })
  },
  methods: {
    dateToYYYYMMDD: function(date){
      return date.getFullYear() + '' + ('0'+ (date.getMonth()+1) ).slice(-2) + '' + ('0' + date.getDate()).slice(-2);
    },
    YYYYMMDDToDate: function(YYYYMMDD){
      return new Date(Number(YYYYMMDD.slice(0, 4)), Number(YYYYMMDD.slice(4, 6)) - 1, Number(YYYYMMDD.slice(6, 8)));
    },
    daySelected: function(e){
      console.log(this.selectedDate)
      this.selectedDate = this.dateToYYYYMMDD(e['date']);
    },
    moveDay: function(int){
      let date = this.YYYYMMDDToDate(this.selectedDate);
      date.setDate(date.getDate() + int);
      this.selectedDate = this.dateToYYYYMMDD(date);
    },
    onValueChange: function(e){
      let key = this.selectedDate + '_' + ('0' + e.hour).slice(-2) + ('0' + e.minute).slice(-2);
      this.$set(this.timeScheduleData, key, e.bool);
      this.$set(this.beforePOSTRequest, key, e.bool);
      this.$nextTick(function(){
        if (!(this.isInAccess)) {
          this.POST();//DOM更新後に送信する
        }
      })
    },
    POST: function () {
      this.isInAccess = true;
      setTimeout(() => {
        let data = {};
        let inProcess = [];
        let counter = 0;
        for (var key in this.beforePOSTRequest) {
          if (counter > 34) { break; }
          data[key] = this.beforePOSTRequest[key];
          inProcess.push(key);
          counter += 1;
        }
        this.axios
          .post(this.jsonUrl, data).then(response => {
            console.log(response);
            this.isProcessError = false;
            for (var key of inProcess) {
              this.$delete(this.beforePOSTRequest, key);
            }
            if (Object.keys(this.beforePOSTRequest).length > 0) {
              this.POST();
            } else {
              this.isInAccess = false;
            }
          }).catch(error => {
            console.log(error);
            this.isInAccess = false;
            if (!error.response) {
              console.log('network error');
              this.isProcessError = true;
              this.errorMessage = '通信に失敗しました。インターネットへの接続を確認し、再度送信ボタンを押してください。(Network Error)'
            } else {
              console.log('internal error');
              this.isProcessError = true;
              this.errorMessage = '処理に失敗しました。変更が保存されていない可能性があります。お手数ですが、開発者までご連絡ください。(' +
                error.response.status + ' ' + error.response.statusText + ')';
            }
          });
      }, 1000);
    }
  },
  computed: {
    YYYYMMDDToTitle: function(){
      if (this.selectedDate == ''){
        return '';
      }
      let year = Number(this.selectedDate.slice(0,4));
      let month = Number(this.selectedDate.slice(4,6));
      let day = Number(this.selectedDate.slice(6,8));
      let date = this.YYYYMMDDToDate(this.selectedDate);
      let jp_weekday = ['日','月','火','水','木','金','土'];
      return month + '月' + day + '日（' + jp_weekday[date.getDay()] + '）';
    },
    selectedDateScheduleData: function (){
      let keys = Object.keys(this.timeScheduleData);
      let matchKeys = keys.filter(item => (item.slice(0,8) === this.selectedDate));
      let data = {};
      for (let key of matchKeys) {
        data[key] = this.timeScheduleData[key]
      }
      return data;
    },
    isActiveDay: function (){
      return (this.selectedDate in this.timeRangeData) && (this.timeRangeData[this.selectedDate].start !== this.timeRangeData[this.selectedDate].end);
    }
  },
  watch: {
    isInAccess: function (newval, oldval) {
      if (newval === false) {
        if (this.whenPageLeave === true) {
          this.afterErrorMessage = '通信が終わりました。もうページを閉じたり、他のページに移動しても大丈夫です。';
          this.whenPageLeave = false;
        }
      }
    }
  }
};

</script>

<style scoped>
section.input-wrap{
  position: relative;
  min-height: 100vh;
}
#menu-switch{
  position: absolute;
  display: block;
  width: 32px;
  height: 32px;
  margin: 8px;
  padding: 0;
  top: 0;
  left: 0;
  background-color: #fff;
  border: none;
  overflow: visible;
  transition: .2s;
  z-index: 20;
}
#menu-switch.active{
  left: 280px;
}
#input-nav{
  position: absolute;
  display: block;
  border: none;
  top: 0;
  left: 0;
  width: 0px;
  padding: 0;
  background-color: #fff;
  transition: .2s;
  overflow: hidden;
  z-index: 10;
}
#input-nav.active{
  width: 280px;
  padding: 0 10px 10px;
  border-right: 1px solid #aaa;
  border-bottom: 1px solid #aaa;
}
div#calendar-wrap{
  width: 260px;
}

#input-form{
  width: 100%;
}
#input-form > h5{
  padding-left: 50px;
}

@media screen and (min-width: 768px) {
#menu-switch{
  display: none;
}
#input-nav{
  position: absolute;
  width: 280px;
  top: 0;
  left: 0;
  padding: 0 10px;
  border-right: 1px solid #aaa;

}
#input-form{
  width: calc(100% - 280px);
  margin-left: 280px;
  padding: 0 10px;
}
#input-form > h5{
  padding-left: 0;
}
}


div.is-in-access{
  position: fixed;
  bottom: 0;
  right: 0;
  margin: 0 1rem;
  padding: 0.25rem;
}
</style>
