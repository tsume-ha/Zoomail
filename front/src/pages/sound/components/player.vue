<template>
  <section>
    <!-- Song Title -->
    <div class="row">
      <div class="col-12" id="songtitle">
        <h4><span>{{nowPlaying.trackNum}}. </span>{{nowPlaying.title}}</h4>
      </div>
    </div>
    
    <!-- wave display -->
    <div v-show="!isReady" id="waveloading" class="p-4">
      <span id="loadtext">{{status.loadSongTitle}}</span>
      <span id="loadprogress">{{status.loadProgressText}}</span>
    </div>
    <div v-show="isReady" id="timedisplay" :style="{marginLeft: status.barProgress + 'px'}">
      <span id="currenttime">{{secondToMMSS(status.currentTime)}}</span> /
      <span id="totaltime">{{secondToMMSS(status.totalTime)}}</span>
    </div>
    <div id="waveform" class=""></div>

    <!-- controller -->
    <div class="row justify-content-around mt-3" id="ctrl">
      <div class="col-xs-2">
        <button id="prev" @click="prev"></button>
      </div>
      <div class="col-xs-2">
        <button id="back" @click="wavesurfer.skip(-10)"></button>
      </div>
      <div class="col-xs-3">
        <button id="start" @click="wavesurfer.playPause()" :class="{getstart:!isPlaying, getstop:isPlaying}"></button>
      </div>
      <div class="col-xs-2">
        <button id="forward" @click="wavesurfer.skip(15)"></button>
      </div>
      <div class="col-xs-2">
        <button id="next" @click="next"></button>
      </div>
    </div>

    <!-- songlist -->
    <div id="songlist" class="row my-3">
      <div
        v-for="song in songs"
        :key="song.path"
        @click="load(song)"
        class="songselect col-sm-12  border-bottom py-1"
        >
        <span class="songnum float-left ml-1 mr-2">{{song.trackNum}}.</span>
        <span class="songname float-left ml-0 pl-0">{{song.title}}</span>
        <span class="download float-right mx-2" @click.stop>
          <a :href="'/sound/download/' + song.id"></a></span>
        <span class="songtime float-right mx-2">{{secondToMMSS(song.length)}}</span>
      </div>
    </div>

  </section>
</template>

<script>
import { computed, onMounted, reactive, ref } from "vue";
import WaveSurfer from "wavesurfer.js";
export default {
  props: {
    songs: {type: Array, required: true}
  },
  setup(props) {
    const nowPlaying = ref({
      id: 0,
      length: 0,
      title: "曲を選択してください",
      trackNum: 0,
      path: "",
    });
    const wavesurfer = ref(null);
    const status = reactive({
      currentTime: null,// 再生している曲の現在位置
      totalTime: null,// 再生している曲の長さ
      barProgress: 0,// プログレスバーの位置(px)
      beforeLoading: true,
      loadSongTitle: "下のリストでロードする曲をクリックしてください",
      loadProgressText: "",
    });

    onMounted(() => {
      wavesurfer.value = WaveSurfer.create({
        container: '#waveform',
        barWidth: 1,
        barHeight: 1.8,
        waveColor: '#33abcc',
        progressColor: '#144552',
        scrollParent: false,
        skipLength: 10,
        normalize: true,
      });
      // イベント登録
      wavesurfer.value.on('loading', (value) => {
        if (value >= 100) {
          status.loadProgressText = ' ...' + String(value) + ' % 波形出力中';
        } else {
          status.loadProgressText = ' ...' + String(value) + ' %';
        }
      });
      wavesurfer.value.on('ready', () => barMoved());
      wavesurfer.value.on('audioprocess', () => barMoved());
      wavesurfer.value.on('seek', () => barMoved());

      // 波形ウィンドウのマウス・タッチ操作
      const wavediv = document.querySelector('#waveform');
      let x;
      const div_width = wavediv.clientWidth;

      wavediv.addEventListener("mousedown", mdown, false);
      wavediv.addEventListener("touchstart", mdown, false);

      function mdown (e) {
        let event;
        if(e.type === "mousedown") {
          event = e;
        } else {
          event = e.changedTouches[0];
        }

        x = event.pageX - this.offsetLeft;
        wavesurfer.value.setVolume(0);
        wavesurfer.value.seekTo(x / div_width);
        barMoved();

        wavediv.addEventListener("mousemove", mmove, false);
        wavediv.addEventListener("touchmove", mmove, false);
        wavediv.addEventListener("mouseup", mup, false);
        wavediv.addEventListener("mouseleave", mup, false);
        wavediv.addEventListener("touchend", mup, false);
        wavediv.addEventListener("touchleave", mup, false);
      }

      function mmove(e) {
        let event;
        if(e.type === "mousemove") {
          event = e;
        } else {
          event = e.changedTouches[0];
        }
        x = event.pageX - this.offsetLeft;
        wavesurfer.value.setVolume(0);
        wavesurfer.value.seekTo(x / div_width);
        barMoved();

        wavediv.addEventListener("mouseup", mup, false);
        wavediv.addEventListener("mouseleave", mup, false);
        wavediv.addEventListener("touchend", mup, false);
        wavediv.addEventListener("touchleave", mup, false);
      }

      function mup() {
        wavediv.removeEventListener("mousemove", mmove, false);
        wavediv.removeEventListener("mouseup", mup, false);
        wavediv.removeEventListener("touchmove", mmove, false);
        wavediv.removeEventListener("touchend", mup, false);
        wavesurfer.value.setVolume(1);
        if (isPlaying.value) {
          wavesurfer.value.play();
        }
      }

    });


    const load = song => {
      nowPlaying.value = {...song};
      status.loadSongTitle = "Now Loading... " + song.title;
      wavesurfer.value.load(song.path);
    };

    const prev = () => {
      if (!isPlaying.value || status.currentTime > 10) {
        const prevsong = props.songs[(props.songs.indexOf(nowPlaying.value) + props.songs.length - 1) % props.songs.length];
        load(prevsong);
        wavesurfer.value.on('ready', () => {
          wavesurfer.value.play();
        });
      } else {
        wavesurfer.value.stop();
      }
    };

    const next = () => {
      const nextsong = props.songs[(props.songs.indexOf(nowPlaying.value) + 1) % props.songs.length];
      load(nextsong);
      wavesurfer.value.on('ready', () => {
        wavesurfer.value.play();
      });
    };

    const barMoved = () => {
      if (wavesurfer.value === null) {
        return 0;
      }
      status.currentTime = parseInt(wavesurfer.value.getCurrentTime());
      status.totalTime = parseInt(wavesurfer.value.getDuration());
      const max_width = document.querySelector("#waveform > wave").clientWidth;
      const bar_width = document.querySelector("#waveform > wave > wave").clientWidth;
      if (bar_width + 90 < max_width) {
        status.barProgress = bar_width;
      } else {
        status.barProgress = bar_width - 90;
      }
    };

    const isReady = computed(() => {
      if (wavesurfer.value === null) {
        return false;
      } else {
        return wavesurfer.value.isReady;
      }
    });
    const isPlaying = computed(() => {
      if (wavesurfer.value === null) {
        return false;
      } else {
        return wavesurfer.value.isPlaying();
      }
    });
    const secondToMMSS = seconds => {
      if (!(typeof seconds === "number")) {
        return 0;
      }
      let minute = Math.floor(seconds / 60);
      let second = seconds % 60;
      second = ('00' + second).slice(-2);
      return minute + ':' + second;
    };

    return {
      wavesurfer, nowPlaying, isReady, isPlaying, status,
      load, prev, next, secondToMMSS
    };
  },
};
</script>


<style scoped>
#return{
	height:24px;
	width:24px;
	display:block;
	position:relative;
	overflow:hidden;
	margin: 3px;
}
#return:before{
	content:'';
	height:12px;
	width:12px;
	display:block;
	border:1px solid #333;
	border-right-width:0;
	border-bottom-width:0;
	transform:rotate(-45deg);-webkit-transform:rotate(-45deg);-moz-transform:rotate(-45deg);-o-transform:rotate(-45deg);-ms-transform:rotate(-45deg);
	position:absolute;
	top:5px;
	left:5px;
}
#return:after{
	content:'';
	height:1px;
	width:20px;
	display:block;
	background:#333;
	position:absolute;
	top:10.5px;
	left:3px;
}

#waveform{
	position: relative;
}
#wavetimeline{
	position: relative;
	display: block;
	background-color: rgba(255,255,255,0.3);
}

div.songselect{
	cursor: pointer;
}

#songtitle h4 span{
	margin-right: 0.5rem;
	font-size: 1.25rem;
}

#ctrl button{
	position: relative;
	min-width: 40px;
	min-height: 40px;
	background-color: #fff;
	border: 1px solid #aaa;
	border-radius: 3px;
}

#prev:before{content:''; height:0; width:0; display:block; border:10px transparent solid; border-left-width:0; border-right-color:#333; position:absolute; top:10px; left:18px;}
#prev:after{content:''; height:20px; width:4px; display:block; background:#333; position:absolute; top:10px; left:12px;}

#back:before{content:''; height:0; width:0; display:block; border:10px transparent solid; border-left-width:0; border-right-color:#333; position:absolute; top:10px; left:18px;}
#back:after{content:''; height:0; width:0; display:block; border:10px transparent solid; border-left-width:0; border-right-color:#333; position:absolute; top:10px; left:8px;}

.getstart:before{content:''; height:0; width:0; display:block; border:10px transparent solid; border-right-width:0; border-left-color:#333; position:absolute; top:10px; left:16px;}
.getstop:before, .getstop:after{content:''; height:20px; width:4px; display:block; background:#333; position:absolute; top:10px; left:14px;}
.getstop:after{left:22px;}
.getstart:after, .getstart:before, .getstop:before, .getstop:after{transition: .2s}

#forward:before{content:''; height:0; width:0; display:block; border:10px transparent solid; border-right-width:0; border-left-color:#333; position:absolute; top:10px; left:12px;}
#forward:after{content:''; height:0; width:0; display:block; border:10px transparent solid; border-right-width:0; border-left-color:#333; position:absolute; top:10px; left:22px;}

#next:before{content:''; height:0; width:0; display:block; border:10px transparent solid; border-right-width:0; border-left-color:#333; position:absolute; top:10px; left:12px;}
#next:after{content:''; height:20px; width:4px; display:block; background:#333; position:absolute; top:10px; left:24px;}


.download a{display:block; position:relative; width:22px; height:22px; border-bottom:2px #333 solid;}
.download a:before{content:''; height:0; width:0; display:block; border:11px transparent solid; border-bottom-width:0; border-top-color:#333; position:absolute; bottom:0px; left:0px; }
.download a:after{content:''; height:10px; width:7px; display:block; background:#333; position:absolute; top:0px; left:7px;}


#songlist span{
	height: 24px;
	overflow: hidden;
}

.songnum{
	width: 21px;
	text-align: right;
}
.songname{
	width: calc(100% - 120px);
}
.songtime{
	width: 30px;
}
.download{
	width: 22px;
}

#waveloading{
	position: absolute;
}

#timedisplay{
	position: absolute;
	height: 18px;
	width: 90px;
	line-height: 16px;
	padding: 1px 2px;
	margin: 110px 0 0 auto;
	text-align: center;
	font-size: 16px;
	background-color: #333;
	color: #eee;
	z-index: 8;
}
</style>
