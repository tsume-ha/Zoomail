$(function(){
    $('#id_written_by option').each(function(index, element){
        $(element).hide();
    });
    $('#id_written_by option[value^=user_year]').each(function(index, element){
        $(element).show();
    });
})

$('#id_year_choice').change(function(){
    selected_year = $(this).val();
    selected_year = String(selected_year);
    console.log(selected_year);
    $('#id_written_by option').each(function(index, element){
        $(element).hide();
    });
    $('#id_written_by option[value^=selected_year]').each(function(index, element){
        $(element).show();
    });
})