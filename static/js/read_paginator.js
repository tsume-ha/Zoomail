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
