function calendar_display(url){
    var request = new XMLHttpRequest();
    request.open('GET', url);
    request.responseType = 'json';
    request.send();
    request.onload = function(){
        let jsondata = request.response;
        console.log(jsondata);
        var timedata = new Vue({
            el: '.day',
            components:{
                data: {
                	json: jsondata
                },
                // timedata:{
                //     props: ['date', 'time'],
                // },
                // methods: {
                //     get_NG_num: function(date, time){
                //         let num = jsondata[date][time];
                //         if (typeof(num) === "undefined") {
                //             console.log('hoge');
                //             return '';
                //         } else {
                //             return ' NG' + String(num);
                //         }
                        
                //     },
                // },
                template: '<div class="time"></div>',
            }
            
        });
    }   
}
