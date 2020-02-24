$(function(){
	$('body').on('touchstart mouseenter', '.room', function(){
	    $(this).addClass('hover');
	}).on('touchend mouseleave','.room' , function(){
	    $(this).removeClass('hover');
	});
})