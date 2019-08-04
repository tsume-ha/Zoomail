const selectors = 'a,div'

$(function(){
	$(selectors)
	.bind('touchstart mouseenter', function(){
	    $(this).addClass('hover');
	}).bind('touchend mouseleave', function(){
	    $(this).removeClass('hover');
	});
})