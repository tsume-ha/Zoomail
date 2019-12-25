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
    },
    methods: {
        window:onload = function() {
            calendar_display(jsonURL, get_room_data);
            console.log(json_calendar);
            console.log(json_roomdata);
        }
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



function get_room_data(){
    const meetingroomURL = 'https://meetingroomcontroller.appspot.com/room/all';
    var request = new XMLHttpRequest();
    request.open('GET', meetingroomURL);
    request.responseType = 'json';
    request.send();
    request.onload = function(){
        json_roomdata = request.response;
        for (var i = 0; i < calendar.days.length; i++) {
            let jsondata = request.response.filter(function(item, index){
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
}


console.log(jsonURL);

})
