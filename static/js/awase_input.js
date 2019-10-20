$('label[for*=can_attend]').click(function(){
	var for_attr = $(this).attr('for');
	var val = $('#'+for_attr).val();
	var attr_list = for_attr.split('-');
	if (Number(attr_list[1]) % 2 == 0) {
		attr_list[1] = String(Number(attr_list[1]) + 1);
		var target = attr_list.join('-');
		$('#'+target).prop('checked', true);
		$('#'+target.slice(0.-2)).val(val);
	}
})
