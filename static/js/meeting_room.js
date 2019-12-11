const requestURL = 'https://meetingroomcontroller.appspot.com/room/today';

var request = new XMLHttpRequest();
request.open('GET', requestURL);
request.responseType = 'json';
request.send();
request.onload = function() {
    console.log(request.response);
}