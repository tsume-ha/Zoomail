$(function(){
    $('#id_invite_user option').each(function(index, element){
        $(element).hide();
    });
    $('#id_invite_user option[value^='+user_year+']').each(function(index, element){
        $(element).show();
    });
})

$('#id_year_choice').change(function(){
    selected_year = $(this).val();
    selected_year = String(selected_year);
    $('#id_invite_user option').each(function(index, element){
        $(element).hide();
    });
    $('#id_invite_user option[value^='+selected_year+']').each(function(index, element){
        $(element).show();
    });
})


let selected_user = []

function adduser(){
    var new_user = $('#id_invite_user').val();
    if (selected_user.indexOf(new_user) == -1) {
        selected_user.push(new_user);
        display(selected_user);
        console.log(new_user);
    }
}

function display(selected_user){
    var display_html = '';
    for (var i = 0; i < selected_user.length; i++) {
        var target = '#id_invite_user option[value=' + selected_user[i] + ']'
        var user_name = $(target).text();
        display_html += '<p data-user="selected_user[i]" class="my-0 mb-1">' + user_name;
        display_html += '<a href="javascript: user_delete("' + selected_user[i] + '")" class="ml-5">削除</a></p>';
    }
    $('#invited_user').html(display_html);
}

function user_delete(user_vaule){
    for(i=0; i<selected_user.length; i++){
        console.log(selected_user[i]);
        console.log(user_vaule);
        if(selected_user[i] == user_vaule){
            selected_user.splice(i, 1);
        }
    }
    display(selected_user);
}