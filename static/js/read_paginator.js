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



// $(window).on('load scroll resize',function(){
//     var page = location.pathname.slice(6, -1);
//     if (page == '') {
//         page = 1;
//     }
//     var target = "li[data-page=" + page + "]"
//     $('ul.pagination li').each(function(){
//         $(this).removeClass('disabled')
//         $(this).children('a').addClass('text-primary')
//         $(this).children('a').removeClass('text-secondary disabled')
//     });
//     $(target).addClass('disabled')
//     $(target).children('a').addClass('text-secondary disabled')
//     $(target).children('a').removeClass('text-primary')
// });      

