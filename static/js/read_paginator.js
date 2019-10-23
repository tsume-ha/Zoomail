$(function(){
    $('#pagination_nav').on('click', function(e){
        $('#page_nav').addClass('checked');
        e.stopPropagation();
    });
    $(document).on('click', function(){
        $('#page_nav').removeClass('checked');
    });
})

var infScroll = new InfiniteScroll( '.content_wrapper', {
    debug: false,
    path: '.next',
    append: '.content',
    checkLastPage: true,
    history: 'push',
    historyTitle: false,
    status: '.page-load-status',
    scrollThreshold: 300,

});

$(window).on('scroll load',function(){
    var page = window.location.pathname.replace('/read/', '').replace('/', '');
    console.log(page);
    $('ul.pagination li').each(function(){
        $(this).removeClass('disabled');
        $(this).children('a').addClass('text-primary');
        $(this).children('a').removeClass('text-secondary disabled');
    });
    $('li[data-num=' + String(page) + ']').addClass('disabled');
    $('li[data-num=' + String(page) + ']').children('a').addClass('text-secondary disabled');
    $('li[data-num=' + String(page) + ']').children('a').removeClass('text-primary');
    if (Number(page) < 5) {
        $('.first').css('display', 'none');
        $('#omit1').css('display', 'none');
        $('#omit2').css('display', 'inline-block');
        $('.last').css('display', 'inline-block');
        for (var i = 1; i <= 5; i++) {
            $('li[data-num=' + i + ']').css('display', 'inline-block');
        }
        for (var i = 6; i <= page_num; i++) {
            $('li[data-num=' + i + ']').css('display', 'none');
        }
    } else if (5 <= Number(page) < page_num - 5) {
        $('.first').css('display', 'inline-block');
        $('#omit1').css('display', 'inline-block');
        $('#omit2').css('display', 'inline-block');
        $('.last').css('display', 'inline-block');
        for (var i = 1; i < Number(page) - 2; i++) {
            $('li[data-num=' + i + ']').css('display', 'none');
        }
        for (var i = Number(page) - 2; i < Number(page) + 3; i++) {
            $('li[data-num=' + i + ']').css('display', 'inline-block');
        }
        for (var i = Number(page) + 3; i <= page_num; i++) {
            $('li[data-num=' + i + ']').css('display', 'none');
        }
    } else {
        $('.first').css('display', 'inline-block');
        $('#omit1').css('display', 'inline-block');
        $('#omit2').css('display', 'none');
        $('.last').css('display', 'none');
    }
});      

