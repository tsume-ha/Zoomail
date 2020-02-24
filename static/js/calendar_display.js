window.addEventListener('DOMContentLoaded', function() {

var json_calendar = [
        {date:'Loading', display_date: 'Loading', display_day: '', room: 'Loading',
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
        detail_dislpay: false,
        detail_date: '',
        detail_time: '',
        detail_list: {},
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
        },
        detail_close: function(event){
            this.detail_dislpay = false;
        },
        detail_open: function(date, time){
            this.detail_dislpay = true;
            this.detail_date = this.days[date].display_date + ' (' + this.days[date].display_day + ')';
            this.detail_time = get_time_range(time);
            this.detail_list = {};
            for (var username in this.days[date].schedule_list){
                let schedule = this.days[date].schedule_list[username][time];
                console.log(schedule);
                let obj = {};
                if (schedule === null || schedule === undefined) {
                    obj.class = 'text-secondary';
                    obj.text = '未回答';
                } else if (schedule === true) {
                    obj.class = 'text-success';
                    obj.text = '○';
                } else if (schedule === false) {
                    obj.class = 'text-danger';
                    obj.text = '×';
                } else {
                    obj.class = "";
                    obj.text = schedule;
                }
                this.detail_list[username] = obj;
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

function get_time_range(time){
    // time--> str  t9_0 or t12_30 etc
    // return --> str 9:00～9:30 etc
    let str = time.replace('t', '');
    str = str.split('_');
    let start = '';
    let end = '';
    if (str[1] == '0') {
        start = str[0] + ':00';
        end = str[0] + ':30';
    } else if (str[1] == '30'){
        start = str[0] + ':30';
        end = String(Number(str[0]) + 1) + ':00';
    }
    return start + '～' + end;
}


})
