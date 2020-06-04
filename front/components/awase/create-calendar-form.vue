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
        <label class="d-block">集計期間:</label>
        <div>
          <v-date-picker
            mode='range'
            v-model='selectedRange'
            :input-props='{class: "form-control"}'
            :min-date="minDate"
            :max-date="maxDate"
            :first-day-of-week='2'
            @input="validate()"
            />
        </div>
        <p v-if="dateError" class="small text-danger pl-2">
          {{dateError}}
        </p>
      </div>
      <input
        type="hidden"
        name="days_begin"
        :value='start' />
      <input
        type="hidden"
        name="days_end"
        :value='end' />

      <input type="submit" value="登録" @click="onclick" class="btn btn-info mx-2 my-3">

    </form>
    <p class="small text-secondary">
    	集計できる期間は現在のところ、最大で120日間です。<br>
    </p>
  </section>
</template>

<script>
export default {
  props: {
    csrftoken: {type: String, required: true},
  },
  data: function () {
    return {
      title: "",
      text: "",
      selectedRange: null,
      dayRangeError: false,
      titleError: "",
      textError: "",
      dateError: "",
      is_sending: false,//送信後画面遷移中のときtrue，多重送信防止
    }
  },
  methods: {
    dateToText: function(date){
      return date.getFullYear() + '-' + ('00' + (date.getMonth() + 1)).slice(-2) + '-' + ('00' + date.getDate()).slice(-2);
    },
    validate: function(){
      let diff = this.selectedRange.end.getTime() - this.selectedRange.start.getTime();
      let days = diff / (1000 * 60 * 60 * 24);
      if (days > 120) {
        this.dayRangeError = true;
      } else {
        this.dayRangeError = false;
      }
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
    start: function(){
      if (this.selectedRange === null) {
        return '';
      } else {
        return this.dateToText(this.selectedRange.start);
      }
    },
    end: function(){
      if (this.selectedRange === null) {
        return '';
      } else {
        return this.dateToText(this.selectedRange.end);
      }
    },
    minDate: function(){
      let dt = new Date();
      return dt;
    },
    maxDate: function(){
      let dt = new Date;
      return dt.setDate(dt.getDate() + 365);
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

      if (this.selectedRange == null) {
        this.dateError = "集計期間を指定してください。";
        return false;
      } else if (this.dayRangeError == true) {
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

<style scoped>

</style>