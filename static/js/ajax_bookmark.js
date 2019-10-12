function bookmark(message_pk) {
    data_text = 'csrfmiddlewaretoken=' + $('input[name="csrfmiddlewaretoken"]').val() + '&message_pk=' + message_pk;
    $.ajax({
         url: location.protocol + '//' + location.host + '/read/ajax_bookmark/' + message_pk + '/',
         method: 'POST',
         data: data_text,
         timeout: 5000,
         dataType: "text",
    })
    .done( function(data) {
        is_marked = data.replace('bookmark=', '')
        if (is_marked == 'true') {
            $('img#img_'+message_pk).attr('src', '/static/img/star_yl.png');
        } else {
            $('img#img_'+message_pk).attr('src', '/static/img/star_bk.png');
        }
    })
    .fail(function() {
    });
}