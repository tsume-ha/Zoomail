window.addEventListener('DOMContentLoaded', function() {

var json_calendar = [
        {date:'Loading', display_date: 'Loading', display_day: '', room: 'Loading',
         NG_list: {t9_0: "", t9_30: "", t10_0: "", t10_30: "", t11_0: "", t11_30: "", t12_0: "", t12_30: "", t13_0: "", t13_30: "", t14_0: "", t14_30: "", t15_0: "", t15_30: "", t16_0: "", t16_30: "", t17_0: "", t17_30: "", t18_0: "", t18_30: "", t19_0: "", t19_30: "", t20_0: "", t20_30: "", t21_0: "", t21_30: "", t22_0: "", t22_30: "", t23_0: "", t23_30: "", t24_0: "", t24_30: "", t25_0: "", t25_30: "", },
         schedule_list: {initial: ''},
        },
    ];
var json_roomdata;
var settings;


var calendar = new Vue({
    el: '#calendar',
    delimiters: ['[|[', ']|]'],
    data: {
        days: json_calendar,
        day_count: 0,
        day_display_max_num: 7,
    },
    methods: {
        window:onload = function() {
            get_calendar_json(jsonURL, get_room_data);
        },
        display_calendar: function(){
            if (this.day_count < 0) {
                this.day_count = 0;
                if (settings.total_days <= this.day_display_max_num) {
                    this.days = json_calendar.slice(this.day_count, settings.total_days);
                } else {
                    this.days = json_calendar.slice(this.day_count, this.day_display_max_num);
                }
            } else if (0 <= this.day_count && this.day_count < settings.total_days - this.day_display_max_num) {
                this.days = json_calendar.slice(this.day_count, this.day_count + this.day_display_max_num);
            } else {
                this.day_count = settings.total_days - this.day_display_max_num;
                this.days = json_calendar.slice(this.day_count, settings.total_days);
            }
        },
        move: function(days){
            this.day_count += days;
            this.display_calendar();
            set_room_data();
        },
        change_display_days: function(day){
            this.day_display_max_num += day;
            if (this.day_display_max_num <= 0) {
                this.day_display_max_num = 1;
            }
            if (settings.total_days <= this.day_display_max_num) {
                this.day_display_max_num = settings.total_days;
            }
            this.display_calendar();
            set_room_data();
        },
        NG_num: function(date, time){
            const NG_class_name = ['NG0', 'NG1', 'NG2', 'NG3'];
            let num = 0;
            let flag = false
            for (var key in this.days[date].schedule_list){
                if (this.days[date].schedule_list[key][time] === false) {
                    num += 1;
                    flag = true;
                } else if (this.days[date].schedule_list[key][time] === true) {
                    flag = true;
                }
            }
            if (flag == false) {
                return '';
            } else if (num < 4) {
                return NG_class_name[num];
            } else {
                return NG_class_name[3];
            }
        }
    },
});


function get_calendar_json(url, callback){
    var request = new XMLHttpRequest();
    request.open('GET', url);
    request.responseType = 'json';
    request.send();
    request.onload = function(){
        json_calendar = request.response.calendar_data;
        settings = request.response.settings;
        calendar.day_count = settings.today_num;
        calendar.display_calendar();
        console.log(json_calendar);
        callback();
    }
}


function set_room_data(){
    for (var i = 0; i < calendar.days.length; i++) {
        let jsondata = json_roomdata.filter(function(item, index){
            if (item.date == calendar.days[i].date) return true;
        });
        if (jsondata.length < 1) {
            calendar.days[i].room = 'NoData';
            continue;
        }
        let display = jsondata[0].room;
        if (display=='終日使用不可') {
            display = '使用不可';
        }
        calendar.days[i].room = display;
        continue;
    }
}



function get_room_data(){
    const meetingroomURL = 'https://meetingroomcontroller.appspot.com/room/all';
    var request = new XMLHttpRequest();
    request.open('GET', meetingroomURL);
    request.responseType = 'json';
    request.send();
    request.onload = function(){
        json_roomdata = request.response;
        set_room_data();
    }
}


})
