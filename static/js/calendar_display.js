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

var data = {
    days: [
        {date:'2019-12-23', display_date: '12/23', display_day: '土', room: 'Loading',},
        {date:'2019-12-24', display_date: '12/24', display_day: '日', room: 'Loading',},
        {date:'2019-12-25', display_date: '12/25', display_day: '月', room: 'Loading',},
        ],
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
