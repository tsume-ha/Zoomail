let app = new Vue({
  el: '#form_upload',
  data: {
    mode: 'single',
    selectedRange: null,
    is_error: false,
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

})

