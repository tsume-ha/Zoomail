<template>
  <section>
    <!-- Live Title -->
    <div class="row border-bottom pb-1 mb-2">
      <div class="col-12">
        <a href="../../" class="float-left col-xs-2" id="return"> </a>
        <h5 class="float-left col-xs-7 ml-2">{{performance.live_name}}</h5>
        <span class="float-right col-xs-3 small">{{performance.recorded_at | date}}</span>
      </div>
    </div>

    <!-- Song Title -->
    <div class="row">
      <div class="col-12" id="songtitle">
        <h4><span>{{nowPlaying.track_num}}. </span>{{nowPlaying.song_name}}</h4>
      </div>
    </div>
    
    <!-- wave display -->
    <div v-show="!isReady" id="waveloading" class="p-4">
      <span id="loadtext">{{loadSongTitle}}</span>
      <span id="loadprogress">{{loadProgressText}}</span>
    </div>
    <div v-show="isReady" id="timedisplay" :style="{marginLeft:barProgress + 'px'}">
      <span id="currenttime">{{currentTime | readableTime}}</span> /
      <span id="totaltime">{{totalTime | readableTime}}</span>
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
        :key="song.fileurl"
        @click="load(song)"
        class="songselect col-sm-12  border-bottom py-1"
        >
        <span class="songnum float-left ml-1 mr-2">{{song.track_num}}.</span>
        <span class="songname float-left ml-0 pl-0">{{song.song_name}}</span>
        <span class="download float-right mx-2"><a
            href="">　</a></span>
        <span class="songtime float-right mx-2">{{song.length | readableTime}}</span>
      </div>
    </div>

  </section>
</template>

<script>
import moment from "moment"
export default {
  props: {
    liveId: {type: Number, required: true}
  },
  data: function () {
    return {
      wavesurfer: null,
      errorMessage: "",
      performance: {},
      songs: [],
      nowPlaying: {
        "id": null,
        "track_num": 0,
        "song_name": "曲を選択してください",
        "fileurl": "",
        "length": 0
      },
      currentTime: null,// 再生している曲の現在位置
      totalTime: null,// 再生している曲の長さ
      barProgress: 0,// プログレスバーの位置(px)
      beforeLoading: true,
      loadSongTitle: "下のリストでロードする曲をクリックしてください",
      loadProgressText: "",

    }
  },
  created: function () {
    this.axios.get('/player/api/live/' + this.liveId)
    .then(response => {
      this.performance = response.data.performance;
      this.songs = response.data.songs;
    })
    .catch(error => {
      this.errorMessage = "通信に失敗しました、もう一度読み込みをしてください。"
    })
  },
  mounted: function () {
    this.$nextTick()
      .then(() => {
        this.wavesurfer = WaveSurfer.create({
          container: '#waveform',
          barWidth: 1,
          barHeight: 1.8,
          waveColor: '#33abcc',
          progressColor: '#144552',
          scrollParent: false,
          skipLength: 10,
          normalize: true,
        })
      }).then(() => {
        // イベント登録
        this.wavesurfer.on('loading', (value) => {
          if (value >= 100) {
            this.loadProgressText = ' ...' + String(value) + ' % 波形出力中';
          } else {
            this.loadProgressText = ' ...' + String(value) + ' %';
          }
        });
        this.wavesurfer.on('ready', () => this.barMoved());
        this.wavesurfer.on('audioprocess', () => this.barMoved());
        this.wavesurfer.on('seek', () => this.barMoved());
        
      }).then(() => {
        //波形ウィンドウのマウス・タッチ操作
        const that = this;
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
          that.wavesurfer.setVolume(0);
          that.wavesurfer.seekTo(x / div_width);
          that.barMoved();

          wavediv.addEventListener("mousemove", mmove, false);
          wavediv.addEventListener("touchmove", mmove, false);
          wavediv.addEventListener("mouseup", mup, false);
          wavediv.addEventListener("mouseleave", mup, false);
          wavediv.addEventListener("touchend", mup, false);
          wavediv.addEventListener("touchleave", mup, false);
        }

        function mmove(e) {
          if(e.type === "mousemove") {
            var event = e;
          } else {
            var event = e.changedTouches[0];
          }
          x = event.pageX - this.offsetLeft;
          that.wavesurfer.setVolume(0);
          that.wavesurfer.seekTo(x / div_width);
          that.barMoved();

          wavediv.addEventListener("mouseup", mup, false);
          wavediv.addEventListener("mouseleave", mup, false);
          wavediv.addEventListener("touchend", mup, false);
          wavediv.addEventListener("touchleave", mup, false);
        }

        function mup(e) {
          wavediv.removeEventListener("mousemove", mmove, false);
          wavediv.removeEventListener("mouseup", mup, false);
          wavediv.removeEventListener("touchmove", mmove, false);
          wavediv.removeEventListener("touchend", mup, false);
          that.wavesurfer.setVolume(1);
          if (that.isPlaying) {
            that.wavesurfer.play();
          }
        }
      });
  },
  methods: {
    prev: function () {
      if (!this.isPlaying || this.currentTime > 10) {
        const prevsong = this.songs[(this.songs.indexOf(this.nowPlaying) + this.songs.length - 1) % this.songs.length];
        this.load(prevsong);
        this.wavesurfer.on('ready', () => {
            this.wavesurfer.play();
        });
      } else {
      this.wavesurfer.stop();
      }
    },
    next: function () {
      const nextsong = this.songs[(this.songs.indexOf(this.nowPlaying) + 1) % this.songs.length];
      this.load(nextsong);
      this.wavesurfer.on('ready', () => {
        this.wavesurfer.play();
      });
    },

    load: function (song) {
      this.nowPlaying = song;
      this.loadSongTitle = "Now Loading... " + song.song_name;
      this.wavesurfer.load(song.fileurl);
    },
    barMoved: function () {
      if (this.wavesurfer == null) {
        return 0;
      }
      this.currentTime = parseInt(this.wavesurfer.getCurrentTime());
      this.totalTime = parseInt(this.wavesurfer.getDuration());
      var max_width = $('#waveform > wave').width();
      var bar_width = $('#waveform > wave > wave').width();
      if (bar_width + 90 < max_width) {
        this.barProgress = bar_width;
      } else {
        this.barProgress = bar_width - 90;
      }
    },
  },
  computed: {
    isReady: function () {
      if (this.wavesurfer == null) {
        return false;
      } else {
        return this.wavesurfer.isReady;
      }
    },
    isPlaying: function () {
      if (this.wavesurfer == null) {
        return false;
      } else {
        return this.wavesurfer.isPlaying();
      }
    },
  },
  filters: {
    date: function (value) {
      return moment(value).format("YYYY/MM/DD")
    },
    readableTime: function (value) {
      let minute = Math.floor(value / 60);
      let second = value % 60;
      second = ('00' + second).slice(-2);
      return minute + ':' + second;
    }
  }
}
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