<template>
  <section id="form_upload" class="my-3">
    <form method="post" enctype="multipart/form-data">
      <input type="hidden" name="csrfmiddlewaretoken" value="2Jde2UmZfD8ZRGYxLcxgBnW4TLdVOm4wuDgXWYp8KMhJatUsrHg6sF37bAzkC8Ao">
      <div class="form-group mx-0">
        <label for="id_title">曲名・バンド名・イベント名:</label>
        <input
          type="text"
          name="title"
          maxlength="200"
          required="required"
          id="id_title"
          class="form-control"
          >
      </div>
      <div class="form-group mx-0">
        <label for="id_text">説明:</label>
        <input
          type="text"
          name="text"
          maxlength="400"
          id="id_text"
          class="form-control">
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
        <p v-if="is_error" class="small text-danger pl-2">
          選択可能な範囲は最大で120日です。
        </p>
      </div>
      <vue-input
        type='hidden'
        name='days_begin'
        init='null'
        :value='start'
        >
      </vue-input>
      <vue-input
        type='hidden'
        name='days_end'
        init='null'
        :value='end'
        >
      </vue-input>

      <input type="submit" value="登録" class="btn btn-info mx-2 my-3">

    </form>
    <p class="small text-secondary">
    	集計できる期間は現在のところ、最大で120日間です。<br>
    </p>
  </section>
</template>

<script>
import inputTag from './form-input-tag.vue';
import DatePicker from 'v-calendar/lib/components/date-picker.umd'
export default {
  components: {
    "vue-input": inputTag,
    "v-date-picker": DatePicker,
  },
  data: function () {
    return {
      mode: 'single',
      selectedRange: null,
      is_error: false,
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
        this.is_error = true;
      } else {
        this.is_error = false;
      }
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
    }


  },

}
</script>

<style scoped>

</style>