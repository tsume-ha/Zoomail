
var wavesurfer = WaveSurfer.create({
	container: '#waveform',
	barWidth: 1,
	waveColor: '#33abcc',
	progressColor: '#144552',
	scrollParent: false,
	skipLength: 10,
	// plugins: [
	// 	WaveSurfer.timeline.create({
	// 		container: "#wavetimeline"
	// 	})
	// ]

});


$(function(){
	wavesurfer.empty();
})



function load(href,title) {
	$('#waveloading').html('Now Loading... ' + title + '<span class="nowloading"> </span>');
	wavesurfer.load(href);
}

wavesurfer.on('ready', function () {
	console.log("done");
	$('#waveloading').css('display','none');
});









$(document).on('click',"#start",function(){
	console.log();
	if (wavesurfer.isPlaying()) {
		//playing => off
		wavesurfer.pause();
		$(this).removeClass('getstop');
		$(this).addClass('getstart');
	} else {
		//not playing => on
		wavesurfer.play();
		$(this).removeClass('getstart');
		$(this).addClass('getstop');
	}
})

$(document).on('click',"#back",function(){
	wavesurfer.skip(-10);
})
$(document).on('click',"#forward",function(){
	wavesurfer.skip(15);
})