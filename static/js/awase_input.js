$('label[for*=can_attend]').click(function(){
    var for_attr = $(this).attr('for');
    var val = $('#'+for_attr).val();
    var attr_list = for_attr.split('-');
    if (Number(attr_list[1]) % 2 == 0) {
        attr_list[1] = String(Number(attr_list[1]) + 1);
        var target = attr_list.join('-');
        $('#'+target).prop('checked', true);
    }
})

$('.dayall').click(function(e){
    e.preventDefault();
    var value = $(this).val();
    date = $(this).data('date');
    target = $('div.form_one_day[data-date='+date+'] input[name$=can_attend][value=' + value + ']');
    target.prop('checked', true);
})

function move_week(direction){
    console.log(direction);
    $('form[name=calendarinput]').attr('action', window.location + '?' + direction + '=True');
    $('form[name=calendarinput]').submit();
}