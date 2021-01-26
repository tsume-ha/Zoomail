<template>
  <div>
    <h3>日程調整を作成</h3>
    <section id="form_upload" class="my-3">
      <form method="post">
        <div class="form-group mx-0">
          <label for="id_title">曲名・バンド名・イベント名:</label>
          <input
            id="id_title"
            class="form-control"
            type="text"
            v-model="title"
            name="title"
            maxlength="64"
            required="required"
            @change="validateTitle"
            >
          <p v-if="titleError" class="small text-danger pl-2">
            {{titleError}}
          </p>
        </div>

        <div class="form-group mx-0">
          <label for="id_text">説明:</label>
          <input
            id="id_text"
            class="form-control"
            type="text"
            v-model="text"
            name="text"
            maxlength="200"
            @change="validateText"
            >
          <p v-if="textError" class="small text-danger pl-2">
            {{textError}}
          </p>
        </div>

        <div class="form-group mx-0">
          <label class="d-block">集計期間:</label>
          <div>
            <v-date-picker
              mode='range'
              v-model='selectedRange'
              :input-props='{class: "form-control"}'
              :min-date="minDate"
              :max-date="maxDate"
              :first-day-of-week='2'
              @input="validateDate"
              />
          </div>
          <p v-if="dateError" class="small text-danger pl-2">
            {{dateError}}
          </p>
        </div>

        <button @click="onclick" class="btn btn-info mx-2 my-3">
          登録
        </button>
      </form>
      <p class="small text-secondary">
        集計できる期間は現在のところ、最大で120日間です。<br>
      </p>
      <nowloading v-if="isSending" text="Now Loading."/>
    </section>
  </div>
</template>

<script>
import moment from "moment";
import nowloading from "../nowloading.vue";
import DatePicker from 'v-calendar/lib/components/date-picker.umd'
export default {
  metaInfo: {
    title: '日程調整を作成'
  },
  components: {
    nowloading,
    'v-date-picker': DatePicker
  },
  data: function () {
    return {
      title: "",
      titleError: "",
      text: "",
      textError: "",
      selectedRange: null,
      dateError: "",
      dayStart: "",// YYYY-MM-DD
      dayEnd: "",// YYYY-MM-DD
      minDate: moment().toDate(),
      maxDate: moment().add(1, 'years').toDate(),
      isSending: false,//送信後画面遷移中のときtrue，多重送信防止
    }
  },
  methods: {
    onclick: function(e){
      e.preventDefault();
      if (this.isSending) {
        return;
      }
      if (this.validateTitle() &&
          this.validateText() &&
          this.validateDate() ) {
        const data = {
          "title": this.title,
          "text": this.text,
          "days_begin": this.dayStart,
          "days_end": this.dayEnd
          };
        console.log(data)
        this.isSending = true;
        this.axios.post("../api/create/", data)
        .then(res => {
          location.href = res.data.url;
          return;
        })
        .catch(error => {
          console.log(error);
          this.isSending = false;
        })
      }
    },
    validateTitle: function () {
      if (this.title.length > 64) {
        this.titleError = "名前が長すぎます。64文字以内で入力してください。";
        return false;
      }
      if (this.title.length == 0) {
        this.titleError = "タイトルは必須です。";
        return false;
      }
      this.titleError = "";
      return true;      
    },
    validateText: function () {
      if (this.text.length > 200) {
        this.textError = "入力が長すぎます。200文字以内で入力してください。";
        return false;
      }
      this.textError = "";
      return true;
    },
    validateDate: function () {
      if (this.selectedRange == null) {
        this.dateError = "集計期間を指定してください。";
        return false;
      }
      const start = moment(this.selectedRange.start);
      const end = moment(this.selectedRange.end);
      if (end.diff(start, 'days') > 120) {
        this.dateError = "集計できる期間は、最大で120日です。";
        return false;
      }
      this.dateError = "";
      this.dayStart = start.format("YYYY-MM-DD");
      this.dayEnd = end.format("YYYY-MM-DD");
      return true;
    }
  }
}
</script>

<style scoped>

</style>