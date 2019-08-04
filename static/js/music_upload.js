const spacer = [' ','-','_','.',]

$(function() {
    $('input[name$=song_file]').on("change", function() {
        var file = this.files[0];
        if(file != null) {
            // console.log(file.name); // ファイル名をログに出力する
            name = file.name;
            for (var i = 0; i < spacer.length; i++) {
            	countrezult = name.indexOf(spacer[i]);
            	if (countrezult < 3) {
            		break;
            	}
            }
            cutname = name.slice(countrezult+1,-4);
            var target_name = $(this).attr('name').replace('file','name');
            var target = 'input[name="' + target_name + '"]';
            $(target).val(cutname);
            var target_span_name = target_name.replace('form-','').replace('-song_name','');
            var target_span_num = Number(target_span_name) + 1;
            var target_span = 'tr:nth-child(' + String(target_span_num) + ') td.file span';
            $(target_span).html(name);
        }
    });
});
