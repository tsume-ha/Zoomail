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
    calendar_json: null,
    meetingroom_json: null,
    days: ['2019-12-23', '2019-12-24', '2019-12-25'],
}

Vue.component('daycolumns', {
	props: ['date'],
	template: '<div class="day column"><div class="date">{{date}}<br>土</div><div class="room">Loading</div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div></div>'
});

var calendar = new Vue({
	el: '#calendar',
	data: data,
});

})

// <div class="day column" data-date="2019-12-21"><div class="date">12/21<br>土</div><div class="room">Loading</div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div></div>