window.onload = function() {

const requestURL = 'https://meetingroomcontroller.appspot.com/room/all';

var request = new XMLHttpRequest();
request.open('GET', requestURL);
request.responseType = 'json';
request.send();
request.onload = function() {
    let jsondata = request.response;
    var room = new Vue({
        el: '.room',
        components:{
            room:{
                props: ['date'],
                methods: {
                    get_room: function(date){
                        let data = jsondata.filter(function(item, index){
                            if (item.date == date) return true;
                        });
                        if (data.length < 1) {
                        	return 'NoData';
                        }
                        let display = data[0].room;
                        console.log(display);
                        if (display=='終日使用不可') {
                            display = '使用不可';
                        }
                        return display;
                    },
                },
                template: '<div>{{get_room(date)}}</div>',
            }
        }
    });

}

}
