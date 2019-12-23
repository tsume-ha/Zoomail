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
        {date:'2019-12-23',display_date: '12/23',display_day: '土'},
        {date:'2019-12-24',display_date: '12/24',display_day: '日'},
        {date:'2019-12-25',display_date: '12/25',display_day: '月'},
        ],
}

Vue.component('daycolumns', {
    data: function(){
        return {
            calendar_json: null,
            meetingroom_json: null,
            hoge:'fuga',
        };
    },
    props: ['date'],
    template: '<div class="day column"><div class="date">{{date}}<br>土{{hoge}}</div><div class="room">Loading</div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div></div>'
});

var calendar = new Vue({
    el: '#calendar',
    data: data,
});

})

// <div class="day column" data-date="2019-12-21"><div class="date">12/21<br>土</div><div class="room">Loading</div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div><div class="time"></div></div>