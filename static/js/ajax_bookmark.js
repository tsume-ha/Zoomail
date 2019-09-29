function bookmark(message_pk) {
// $('#resultPOST').text('通信中...');
    // Ajax通信を開始
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
    	pk = data.replace('bookmark=', '')
		if (pk) {
			$('img#img_'+message_pk).attr('src', '/static/img/star_yl.png');
		} else {
			$('img#img_'+message_pk).attr('src', '/static/img/star_bk.png');
		}
    })
    .fail(function() {
        // 通信失敗時の処理を記述
        // $('#resultPOST').text('POST処理失敗.');
    });
}