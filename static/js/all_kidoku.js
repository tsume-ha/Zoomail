function kidoku() {
    var result = confirm('【確認】　すべての未読メッセージを既読にしますか？');
 
    if(result) {
		$.post(location.href,$('#kidoku_form').serialize()
		);
    } else {
    // 戻る
    }
}