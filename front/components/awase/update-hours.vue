<template>
<div>
  <h3>集計時間を変更</h3>
  <p class="mb-4">
      各日にちの中で日程調整したい時間帯を変更できます。<br>
      時間は24時間表記で、9時(AM9:00)～26時(翌AM2:00)まで1時間単位で指定できます。<br>
      また、期間内の任意の日を、「集計しない日」に設定することも出きます。
  </p>
  <div v-if="!jsonLoaded">
    <p>読み込み中...</p>
  </div>
  <div v-else>
    <div v-if="isProcessError">
      <p v-text="errorMessage" class="text-danger"></p>
    </div>
    <h6>1. 日付をクリックして変更したい日(複数も可)を選ぶ</h6>
    <v-calendar
      :first-day-of-week="2"
      is-expanded
      :columns="$screens({ default: 1, md: 2 })"
      >
      <template slot='header-title' slot-scope='props'>
        {{props.yearLabel}}年{{props.monthLabel}}
      </template>
      <template slot='day-content' slot-scope='props'>
        <custom-day-content
          :day="props.day"
          :data="timedata[dateToYYYYMMDD(props.day.date)]"
          :is-selected="(props.day.id in selectedDate)"
          @dayadd="dayadd"
          @dayremove="dayremove"></custom-day-content>
      </template>

    </v-calendar>
    <hr>
    <h6>2. 選んだ日に対して、集計時間を設定するか、集計しない日にするか指定する。</h6>
    <div id="time-select" class="row my-3 mx-2">
      <time-selector name="start" :max="end" @onchange="timeChange"></time-selector>
      <span class="m-2">から</span>
      <time-selector name="end" :min="start" @onchange="timeChange"></time-selector>
      <span class="m-2">に</span>
      <button @click="setTimeData" class="btn btn-info">変更</button>
    </div>
    <div id="not-collect-select" class="row my-3 mx-2">
      <span class="m-2">もしくは、</span>
      <button @click="setNotCollectDay" class="btn btn-secondary">「集計しない日」にする</button>
    </div>
    <div v-if="isInAccess" class="small text-secondary is-in-access">サーバーと通信中...</div>
    <hr>  
    <router-link to="../" class="btn btn-secondary mx-2 my-3">戻る</router-link>
  </div>
</div>
</template>

<script>
import customDayContent from './update-hours-custom-day-content.vue';
import timeSelector from './update-hours-time-selector.vue';
export default {
  metaInfo: {
    title: '集計時間を変更'
  },
  components: {
    "custom-day-content": customDayContent,
    "time-selector": timeSelector,
  },
  data: function () {
    return {
      jsonLoaded: false,
      isProcessError: false,
      errorMessage: '',
      isInAccess: false,
      timedata: {},
      selectedDate: {},
      start: null,
      end: null,
      beforePOSTRequest: {},
    }
  },
  created: function(){  
    this.axios
      .get('./json/')
      .then((res) => {
        this.timedata = res.data;
        this.jsonLoaded = true;
      }).catch((error) => {
        console.log(error);
        this.$router.push({name: '404'})
      });
  },
  methods: {
    dayadd: function(e){
      let id = e.id;
      if (!(id in this.selectedDate)) {
        this.$set(this.selectedDate, id, e);
      }
    },
    dayremove: function(e){
      let id = e.id;
      if (id in this.selectedDate) {
        this.$delete(this.selectedDate, id);
      }
    },
    clear: function(){
      this.selectedDate = {};
    },
    timeChange: function(e){
      this[e.name] = e.value;
    },
    setTimeData: function(){
      if (this.start === null && this.end === null) {
        return false;
      }
      for (const day in this.selectedDate) {
        let content = this.selectedDate[day];
        let key = this.dateToYYYYMMDD(content.date);
        if (this.start){
          this.$set(this.timedata[key], 'start', this.start);
        }
        if (this.end) {
          this.$set(this.timedata[key], 'end', this.end);
        }
        if (this.timedata[key].start > this.timedata[key].end) {
          console.log('validation error');
          if (this.start === null) {
            this.$set(this.timedata[key], 'start', 9);
          } else if (this.end === null) {
            this.$set(this.timedata[key], 'end', 26);
          } else {
            this.$set(this.timedata[key], 'start', 9);
            this.$set(this.timedata[key], 'end', 26);
          }
        }
        this.$set(this.beforePOSTRequest, key, this.timedata[key]);
        this.$delete(this.selectedDate, day);
      }
      this.postMethod();
    },
    setNotCollectDay: function(){
      for (const day in this.selectedDate) {
        let content = this.selectedDate[day];
        let key = this.dateToYYYYMMDD(content.date);

        this.$set(this.timedata[key], 'start', 9);
        this.$set(this.timedata[key], 'end', 9);

        this.$set(this.beforePOSTRequest, key, this.timedata[key]);
        this.$delete(this.selectedDate, day);
      }
      this.postMethod();
    },
    postMethod: function(){
      this.isInAccess = true;
      let data = {};
      let inProcess = [];
      let counter = 0;
      for (var key in this.beforePOSTRequest) {
        if (counter > 10) {break;}
        data[key] = this.beforePOSTRequest[key].start + '-' + this.beforePOSTRequest[key].end;
        inProcess.push(key);
        counter += 1;
      }

      this.axios
        .post('./json/', data).then((response) => {
          console.log(response);
          this.isProcessError = false;
          for (var key of inProcess) {
            this.$delete(this.beforePOSTRequest, key);
          }

          if (Object.keys(this.beforePOSTRequest).length > 0) {
            this.postMethod();
          } else {
            this.isInAccess = false;
          }
        })
        .catch((error) => {
          console.log(error);
          this.isInAccess = false;
          if (!error.response.status) {
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
    },
    dateToYYYYMMDD: function(date){
      return date.getFullYear() + '' + ('0'+ (date.getMonth()+1) ).slice(-2) + '' + ('0' + date.getDate()).slice(-2);
    }
  },
}
</script>

<style scoped>
div.is-in-access{
    position: fixed;
    bottom: 0;
    right: 0;
    margin: 0 1rem;
    padding: 0.25rem;
}
</style>