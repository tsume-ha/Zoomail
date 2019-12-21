const jsonrequestURL = 'http://localhost:3333/awase/calendar/json/4/';

var request = new XMLHttpRequest();
request.open('GET', jsonrequestURL);
request.responseType = 'json';
request.send();
request.onload = function() {
    let jsondata = request.response;

}

