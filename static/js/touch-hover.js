$(function(){
	$("document *")
	.bind('touchstart', function(){
	    $(this).addClass('hover');
	}).bind('touchend', function(){
	    $(this).removeClass('hover');
	});
})