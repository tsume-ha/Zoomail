<template>
  <section id="form_upload" class="my-3">
    <form method="post">
      <input type="hidden" name="csrfmiddlewaretoken" :value="csrftoken">
      <div class="form-group mx-0">
        <label for="id_title">曲名・バンド名・イベント名:</label>
        <input
          type="text"
          v-model="title"
          name="title"
          maxlength="200"
          required="required"
          id="id_title"
          class="form-control"
          >
        <p v-if="titleError" class="small text-danger pl-2">
          {{titleError}}
        </p>
      </div>
      <div class="form-group mx-0">
        <label for="id_text">説明:</label>
        <input
          type="text"
          v-model="text"
          name="text"
          maxlength="400"
          id="id_text"
          class="form-control">
        <p v-if="textError" class="small text-danger pl-2">
          {{textError}}
        </p>
      </div>
      <div class="form-group mx-0">
        <label class="d-block">はじめ:</label>
        <div>
          <v-date-picker
            v-model="begin"
            mode="single"
          ></v-date-picker>
        </div>
      </div>
      <div class="form-group mx-0">
        <label class="d-block">おわり:</label>
        <div>
          <v-date-picker
            v-model="end"
            mode="single"
          ></v-date-picker>
        </div>
      </div>
      <p v-if="dateError" class="small text-danger pl-2">
        {{dateError}}
      </p>
      <input
        type="hidden"
        name="days_begin"
        :value='daysBegin' />
      <input
        type="hidden"
        name="days_end"
        :value='daysEnd' />

      <input type="submit" value="変更" @click="onclick" class="btn btn-info mx-2 my-3">

    </form>
    <p class="small text-secondary" @click="onclick">
      集計できる期間は現在のところ、最大で120日間です。<br>
    </p>
    <a href="../" class="btn btn-secondary mx-2 my-3">戻る</a>
  </section>
</template>



<script>
import moment from "moment"
import DatePicker from 'v-calendar/lib/components/date-picker.umd'
export default {
  components: {
    'v-date-picker': DatePicker
  },
  props: {
    csrftoken: {type: String, required: true},
    initTitle: {type: String, required: true},
    initText: {type: String, required: false, default: ""},
    initDaysBegin: {type: String, required: true},// YYYY-MM-DD
    initDaysEnd: {type: String, required: true},// YYYY-MM-DD
  },
  data: function () {
    return {
      title: "",
      text: "",
      begin: null,
      end: null,
      titleError: "",
      textError: "",
      dateError: "",
      is_sending: false,//送信後画面遷移中のときtrue，多重送信防止
    }
  },
  created: function () {
    this.title = this.initTitle
    this.text = this.initText
    this.begin = new Date(moment(this.initDaysBegin, "YYYY-MM-DD").format())
    this.end = new Date(moment(this.initDaysEnd, "YYYY-MM-DD").format())
  },
  methods: {
    dateToText: function(date){
      return date.getFullYear() + '-' + ('00' + (date.getMonth() + 1)).slice(-2) + '-' + ('00' + date.getDate()).slice(-2);
    },
    onclick: function(e){
      if (!this.is_valid) {
        e.preventDefault();
        return false;
      }
      if (this.is_sending) {
        e.preventDefault();
        return false;
      }
      this.is_sending = true;
    }
  },
  computed: {
    daysBegin: function(){
      if (this.begin === null) {
        return '';
      } else {
        return this.dateToText(this.begin);
      }
    },
    daysEnd: function(){
      if (this.end === null) {
        return '';
      } else {
        return this.dateToText(this.end);
      }
    },
    is_valid: function () {

      if (this.title.length > 100) {
        this.titleError = "名前が長すぎます。100文字以内で入力してください。";
        return false;
      } else {
        this.titleError = "";
      }

      if (this.title.length == 0) {
        this.titleError = "曲名・バンド名の入力は必須です。";
        return false;
      } else {
        this.titleError = "";
      }

      if (this.text.length > 200) {
        this.textError = "入力が長すぎます。200文字以内で入力してください。";
        return false;
      } else {
        this.textError = "";
      }

      if (this.begin == null || this.begin == "") {
        this.dateError = "集計開始日にちを指定してください。";
        return false;
      } else if(this.end == null || this.end == "") {
        this.dateError = "集計終了日にちを指定してください。";
        return false;
      }
      
      let diff = this.end.getTime() - this.begin.getTime();
      let days = diff / (1000 * 60 * 60 * 24);
      if (diff < 0) {
        this.dateError = "集計開始日は、集計終了日よりも前に設定してください。";
        return false;
      } else if (days > 120) {
        this.dateError = "集計可能な期間は最大120日です";
        return false;
      } else {
        this.dateError = "";
      }

      return true;

    }
  },

}
</script>
