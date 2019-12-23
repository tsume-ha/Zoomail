function calendar_display(url){
    // var request = new XMLHttpRequest();
    // request.open('GET', url);
    // request.responseType = 'json';
    // request.send();
    // request.onload = function(){
    //     let jsondata = request.response;
    //     console.log(jsondata);
    //     var timedata = new Vue({
    //         el: '.day',
    //         data: jsondata,            
    //     });
    // }
}

window.addEventListener('DOMContentLoaded', function() {

const json_calendar = [
        {date:'2019-12-23', display_date: '12/23', display_day: '土', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-24', display_date: '12/24', display_day: '日', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-25', display_date: '12/25', display_day: '月', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-26', display_date: '12/26', display_day: '土', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-27', display_date: '12/27', display_day: '日', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-28', display_date: '12/28', display_day: '月', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-29', display_date: '12/29', display_day: '土', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-30', display_date: '12/30', display_day: '日', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
        {date:'2019-12-31', display_date: '12/31', display_day: '月', room: 'Loading', NGlist: [1,2,3,1,2,3,1,2,3,3,3,3,3,3,3,3,3,]},
    ];

var data = {
    days: json_calendar.slice(0,5),
}


var calendar = new Vue({
    el: '#calendar',
    delimiters: ['[|[', ']|]'],
    data: data,
});

(function () {
    const meetingroomURL = 'https://meetingroomcontroller.appspot.com/room/all';
    var request = new XMLHttpRequest();
    request.open('GET', meetingroomURL);
    request.responseType = 'json';
    request.send();
    request.onload = function(){
	    for (var i = 0; i < data.days.length; i++) {
	    	let jsondata = request.response.filter(function(item, index){
                if (item.date == data.days[i].date) return true;
            });
            if (jsondata.length < 1) {
                data.days[i].room = 'NoData';
            }
            let display = jsondata[0].room;
            if (display=='終日使用不可') {
                display = '使用不可';
            }
            data.days[i].room = display;
	    }
	}
}());

})
