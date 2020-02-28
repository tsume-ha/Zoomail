var submit_clicked = false;
$('form#SendMessageForm').submit(function() {
    if (!submit_clicked) {// 1回目
        submit_clicked = true;
    } else {// 2回目以降
        return false;
    }
});