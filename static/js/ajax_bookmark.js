function bookmark(message_pk) {
    var data_text = 'csrfmiddlewaretoken=' + $('input[name="csrfmiddlewaretoken"]').val() + '&message_pk=' + message_pk;
    var before_ajax = $('img#img_'+message_pk).attr('src');
    if (before_ajax == '/static/img/star_yl.png') {
        $('img#img_'+message_pk).attr('src', '/static/img/star_bk.png');
    } else {
        $('img#img_'+message_pk).attr('src', '/static/img/star_yl.png');
    }
    $.ajax({
         url: location.protocol + '//' + location.host + '/read/ajax_bookmark/' + message_pk + '/',
         method: 'POST',
         data: data_text,
         timeout: 5000,
         dataType: "text",
    })
    .done(function(data){
        var is_marked = data.replace('bookmark=', '')
        if (is_marked == 'true') {
            $('img#img_'+message_pk).attr('src', '/static/img/star_yl.png');
        } else {
            $('img#img_'+message_pk).attr('src', '/static/img/star_bk.png');
        }
    })
    .fail(function(){
        $('img#img_'+message_pk).attr('src', before_ajax);
        console.log('通信失敗：ブックマーク処理');
        $('.popup').html('<p>ブックマークの通信ができませんでした。<br>時間をおいて再度行ってください。</p>');
        $('.popup').fadeIn(1000, function(){
            setTimeout(function(){
                $('.popup').fadeOut(500);
            },3000);
        });
    });
}