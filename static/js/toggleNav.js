function toggleNav() {
    var checkbox = document.getElementById('nav-open');
    // chekcbox の値をtoggleする
    checkbox.checked = !checkbox.checked;
    // 手動でイベントを発火する
    var event = new Event('change');
    checkbox.dispatchEvent(event);
}