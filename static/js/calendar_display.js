window.addEventListener('DOMContentLoaded', function() {

var json_calendar = [
        {date:'Loading', display_date: 'Loading', display_day: '', room: 'Loading', NGlist: ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',]},
    ];
var json_roomdata;

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
            calendar_display(jsonURL, get_room_data);
        },
        move: function(days){
            calendar.day_count += days;
            if (calendar.day_count < 0) {
                calendar.day_count = 0;
            }
            calendar.days = json_calendar.slice(calendar.day_count, calendar.day_count + calendar.day_display_max_num);
            set_room_data();
        },
    }
});


function calendar_display(url, callback){
    var request = new XMLHttpRequest();
    request.open('GET', url);
    request.responseType = 'json';
    request.send();
    request.onload = function(){
        json_calendar = request.response.calendar_data;
        calendar.days = json_calendar.slice(0,7);
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
