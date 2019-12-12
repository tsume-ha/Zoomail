window.onload = function() {
const requestURL = 'https://meetingroomcontroller.appspot.com/room/today';

var request = new XMLHttpRequest();
request.open('GET', requestURL);
request.responseType = 'json';
request.send();
request.onload = function() {
	let data = request.response;
    let mm = data.date.substr(5,2);
    let dd = data.date.substr(8,2);
    let month = Number(mm);
    let date = Number(dd);
    let displaydate = month + '/' + date;
    var meetingroom = new Vue({
    	el: '#meeting_room',
    	delimiters: ['[|[', ']|]'],// Vueの{{hoge}}がdjangoとかぶるので、[|[hoge]|]に変えてみます
    	data: {
    		today: displaydate,
    		room: data.room
    	}
    })
}

}
