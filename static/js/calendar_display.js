window.addEventListener('DOMContentLoaded', function() {

var json_calendar = [
        {date:'Loading', display_date: 'Loading', display_day: '', room: 'Loading', NGlist: ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',]},
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
        }
    }
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
