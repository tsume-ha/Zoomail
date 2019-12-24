window.addEventListener('DOMContentLoaded', function() {

var json_calendar = [
        {date:'Loading', display_date: 'Loading', display_day: '', room: 'Loading', NGlist: ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',]},
    ];


var calendar = new Vue({
    el: '#calendar',
    delimiters: ['[|[', ']|]'],
    data: {
        days: json_calendar,
    },
});
(function () {
	function calendar_display(url){
	    var request = new XMLHttpRequest();
	    request.open('GET', url);
	    request.responseType = 'json';
	    request.send();
	    request.onload = function(){
            json_calendar = request.response.calendar_data
	        calendar.days = json_calendar.slice(0,7);
console.log(calendar.days);
	    }
	}
	calendar_display('http://localhost:3333/awase/calendar/json/4/');
}());

(function () {
    const meetingroomURL = 'https://meetingroomcontroller.appspot.com/room/all';
    var request = new XMLHttpRequest();
    request.open('GET', meetingroomURL);
    request.responseType = 'json';
    request.send();
    request.onload = function(){
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
}());


})
