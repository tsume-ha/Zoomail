$(function(){
	var saved_title = localStorage.getItem('title');
	var saved_content = localStorage.getItem('content');
	if (saved_title != null || saved_content != null) {
		if (saved_title == null) {saved_title = "（入力なし）";}
		if (saved_content == null) {saved_content = "（入力なし）";}
		const text = '<h5>前回終了時に自動保存されたメッセージがあります。</h5><p>件名 : ' + saved_title + '<br>本文 : ' + saved_content.substring(0,50) + 
					 '</p><p>復元しますか？<a href="javascript:restore();" class="ml-4 p-2 alert-link">はい</a><a href="javascript:cancel_restore();" class="ml-3 p-2 alert-link ">いいえ</a></p>';
		$('#SaveDataInfo').html(text);
		$('#SaveDataInfo').fadeIn(400);
	}
})
function restore(){
	var saved_title = localStorage.getItem('title');
	var saved_content = localStorage.getItem('content');
	if (saved_title != null) {$('#id_title').val(saved_title);}
	if (saved_content != null) {$('#id_content').val(saved_content);}
	$('#SaveDataInfo').fadeOut(600);
}

function cancel_restore(){
	$('#SaveDataInfo').fadeOut(400);
}

$('input, select, textarea').change(function(){
	// 宛先を未選択のとき
	var is_error = $('#id_to').val() == 'error';
	if (is_error) {
		$('#id_to').addClass("is-invalid");
	}　else {
		$('#id_to').removeClass("is-invalid");
	}

	// title storage保存
	var title = $('#id_title').val();
	if (title == "") {} else {
		localStorage.setItem("title",title);
	}
	var saved_title = localStorage.getItem('title');

	// content storage保存
	var content = $('#id_content').val();
	if (content == "") {} else {
		localStorage.setItem("content",content);
	}
	var saved_content = localStorage.getItem('content');
})


$('#SendMessageForm').submit(function(){
	var is_error = $('#id_to').val() == 'error';
	if (is_error) {
		$('#id_to').addClass("is-invalid");
		return false;
	}

	// when everything is successed
	// delete local storage
	
	// localStorage.clear();// DBにデータを複製するためにOFFにしておきます

})