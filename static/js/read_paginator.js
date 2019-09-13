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
    debug: true,
    path: '.next',
    append: '.content',
    checkLastPage: true,
    history: 'push',
    historyTitle: false,
    status: '.page-load-status',
    scrollThreshold: 300,

});



$(window).on('load scroll resize',function(){
    var path = location.search;
    var now_page = path.slice(path.indexOf("?page=")+6)
    if (now_page == '') {
        now_page = 1;
    }
    var target = "li[data-page=" + now_page + "]"
    $('ul.pagination li').each(function(){
        $(this).removeClass('disabled')
        $(this).children('a').addClass('text-primary')
        $(this).children('a').removeClass('text-secondary disabled')
    });
    $(target).addClass('disabled')
    $(target).children('a').addClass('text-secondary disabled')
    $(target).children('a').removeClass('text-primary')
});      

