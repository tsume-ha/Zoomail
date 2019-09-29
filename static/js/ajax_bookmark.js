function bookmark(message_pk) {
    data_text = 'csrfmiddlewaretoken=' + $('input[name="csrfmiddlewaretoken"]').val() + '&message_pk=' + message_pk;
    console.log(location.protocol + '//' + location.host + '/read/ajax_bookmark/' + message_pk + '/')
    $.ajax({
         url: location.protocol + '//' + location.host + '/read/ajax_bookmark/' + message_pk + '/',
         method: 'POST',
         data: data_text,
         timeout: 5000,
         dataType: "text",
    })
    .done( function(data) {
    	console.log(data);
    	pk = data.replace('bookmark=', '')

    	console.log(pk);
		if (pk == 'true') {
			$('img#img_'+message_pk).attr('src', '/static/img/star_yl.png');
		} else {
			$('img#img_'+message_pk).attr('src', '/static/img/star_bk.png');
		}
    })
    .fail(function() {
    });
}