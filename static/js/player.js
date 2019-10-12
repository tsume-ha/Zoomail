var wavesurfer = WaveSurfer.create({
	container: '#waveform',
	barWidth: 1,
	barHeight: 1.8,
	waveColor: '#33abcc',
	progressColor: '#144552',
	scrollParent: false,
	skipLength: 10,
	normalize: true,

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
	$('#loadtext').text('Now Loading... ' + title);
	$('#songtitle').html('<h4><span>' + number + '.</span>' + title + '</h4>');
	wavesurfer.load(href);
	PlayingFileNum = Number(number);
}

wavesurfer.on('ready', function () {
	$('#waveloading').css('display','none');

    // var timeline = Object.create(WaveSurfer.Timeline);
    // timeline.init({
    //     wavesurfer: wavesurfer,
    //     container: '#wavetimeline'
    // });
});


wavesurfer.on('loading', function (value) {
	if (value >= 100) {
		$('#loadprogress').text(' ...' + String(value) + ' % 波形出力中');
	} else {
		$('#loadprogress').text(' ...' + String(value) + ' %');
	}
	
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
	NextNum = (Number(PlayingFileNum) % Number(AllFileNum)) + 1;
	target = '#songlist>div:nth-child(' + NextNum + ')';
	url = $(target).data('url');
	title = $(target).data('name');
	load(url,NextNum,title);
	wavesurfer.on('ready', function(){
		music_start();
	});
})
$(document).on('click',"#prev",function(){
	var currenttime = wavesurfer.getCurrentTime();
	if (currenttime < 10) {
		NextNum = (Number(PlayingFileNum) + Number(AllFileNum) - 2) % Number(AllFileNum) + 1;
		target = '#songlist>div:nth-child(' + NextNum + ')';
		url = $(target).data('url');
		title = $(target).data('name');
		load(url,NextNum,title);
		wavesurfer.on('ready', function(){
			music_start();
		});
	} else {
		wavesurfer.stop();
		music_pause();
	}
})


