var wavesurfer = WaveSurfer.create({
	container: '#waveform',
	barWidth: 1,
	barHeight: 1.8,
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

var PlayingFileNum = 0;
var AllFileNum = $('#songlist>div:last-child').data('track');

$(function(){
	wavesurfer.empty();
})


function music_pause(){
	wavesurfer.pause();
	$('#start').removeClass('getstop');
	$('#start').addClass('getstart');
}

function music_start(){
	if (wavesurfer.isPlaying()) {
		//playing => off
		music_pause();
	} else {
		//not playing => on
		wavesurfer.play();
		$('#start').removeClass('getstart');
		$('#start').addClass('getstop');
	}
}


function load(href,number,title) {
	music_pause();
	$('#waveloading').css('display','block');
	$('#waveloading').html('Now Loading... ' + title + '<span class="nowloading"> </span>');
	$('#songtitle').html('<h4><span>' + number + '.</span>' + title + '</h4>');
	wavesurfer.load(href);
	PlayingFileNum = number;
}

wavesurfer.on('ready', function () {
	$('#waveloading').css('display','none');
});







$(document).on('click',"#start",function(){
	if (PlayingFileNum != 0) {
		music_start();
	}
})

$(document).on('click',"#back",function(){
	wavesurfer.skip(-10);
})
$(document).on('click',"#forward",function(){
	wavesurfer.skip(15);
})
$(document).on('click',"#next",function(){
	music_pause();
	NextNum = (PlayingFileNum % AllFileNum) + 1;
	target = '#songlist>div:nth-child(' + NextNum + ')';
	url = $(target).data('url');
	title = $(target).data('name');
	load(url,NextNum,title);
	wavesurfer.on('ready', function(){
		music_start();
	});
})
$(document).on('click',"#prev",function(){
	music_pause();
	NextNum = (PlayingFileNum + AllFileNum - 2) % AllFileNum + 1;
	target = '#songlist>div:nth-child(' + NextNum + ')';
	url = $(target).data('url');
	title = $(target).data('name');
	load(url,NextNum,title);
	wavesurfer.on('ready', function(){
		music_start();
	});
})


