<template>
  <section id="wave-wrapper" class="card">

    <!-- Song Title -->
    <h4 id="songtitle">{{nowPlaying.trackNum}}. {{nowPlaying.title}}</h4>
    
    <!-- wave display -->
    <div v-show="!isReady" id="waveloading">
      <span id="loadtext">{{status.loadSongTitle}}</span>
      <span id="loadprogress" class="text-break">{{status.loadProgressText}}</span>
    </div>
    <div v-show="isReady" id="timedisplay" :style="{marginLeft: status.barProgress + 'px'}">
      <span id="currenttime">{{secondToMMSS(status.currentTime)}}</span> /
      <span id="totaltime">{{secondToMMSS(status.totalTime)}}</span>
    </div>
    <div id="waveform" class=""></div>

    <!-- controller -->
    <div id="controller" class="pure-g">
      <button id="prev" @click="prev" class="pure-u-1-5">
        <Icon :icon="['fas', 'step-backward']" />
      </button>
      <button id="back" @click="wavesurfer.skip(-10)" class="pure-u-1-5">
        <Icon :icon="['fas', 'backward']" />
      </button>
      <button id="start" @click="wavesurfer.playPause()" :class="{getstart:!isPlaying, getstop:isPlaying}" class="pure-u-1-5">
        <Icon :icon="['fas', 'play']" v-if="!isPlaying" />
        <Icon :icon="['fas', 'stop']" v-if="isPlaying" />
      </button>
      <button id="forward" @click="wavesurfer.skip(15)" class="pure-u-1-5">
        <Icon :icon="['fas', 'forward']" />
      </button>
      <button id="next" @click="next" class="pure-u-1-5">
        <Icon :icon="['fas', 'step-forward']" />
      </button>

    </div>

    <!-- songlist -->
    <div id="songlist" class="pure-menu">
      <ul class="pure-menu-list">
        <li
          v-for="song in songs"
          :key="song.id"
          class="pure-menu-item"
        >
        <div @click="load(song)" class="pure-menu-link song-row">
          <span class="songnum">{{song.trackNum}}.</span>
          <span class="songname">{{song.title}}</span>
          <span class="songtime">{{secondToMMSS(song.length)}}</span>
          <a
            :href="`/download/sound/${song.id}/`"
            class="download"
          ><Icon icon="download" /></a>
        </div>
        </li>
      </ul>
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
        container: "#waveform",
        barWidth: 1,
        barHeight: 1.8,
        waveColor: "#33abcc",
        progressColor: "#144552",
        scrollParent: false,
        skipLength: 10,
        normalize: true,
      });
      // イベント登録
      wavesurfer.value.on("loading", (value) => {
        if (value >= 100) {
          status.loadProgressText = ` ...${String(value)} % 波形出力中`;
        } else {
          status.loadProgressText = ` ...${String(value)} %`;
        }
      });
      wavesurfer.value.on("ready", () => barMoved());
      wavesurfer.value.on("audioprocess", () => barMoved());
      wavesurfer.value.on("seek", () => barMoved());

      // 波形ウィンドウのマウス・タッチ操作
      const wavediv = document.querySelector("#waveform");
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
        // this: element
        x = event.pageX - this.getBoundingClientRect().left;
        wavesurfer.value.setVolume(0);
        wavesurfer.value.seekTo(Math.max(0, Math.min((x / div_width), 1)));
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
        // this: element
        x = event.pageX - this.getBoundingClientRect().left;
        wavesurfer.value.setVolume(0);
        wavesurfer.value.seekTo(Math.max(0, Math.min((x / div_width), 1)));
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
      status.loadSongTitle = `Now Loading... ${song.title}`;
      wavesurfer.value.load(song.path);
    };

    const prev = () => {
      if (!isPlaying.value || status.currentTime > 10) {
        const prevsong = props.songs[(props.songs.indexOf(nowPlaying.value) + props.songs.length - 1) % props.songs.length];
        load(prevsong);
        wavesurfer.value.on("ready", () => {
          wavesurfer.value.play();
        });
      } else {
        wavesurfer.value.stop();
      }
    };

    const next = () => {
      const nextsong = props.songs[(props.songs.indexOf(nowPlaying.value) + 1) % props.songs.length];
      load(nextsong);
      wavesurfer.value.on("ready", () => {
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
      if (bar_width + 110 < max_width) {
        status.barProgress = bar_width;
      } else {
        status.barProgress = bar_width - 110;
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
      const minute = Math.floor(seconds / 60);
      let second = seconds % 60;
      second = (`00${second}`).slice(-2);
      return `${minute}:${second}`;
    };

    return {
      wavesurfer, nowPlaying, isReady, isPlaying, status,
      load, prev, next, secondToMMSS
    };
  },
};
</script>


<style lang="scss" scoped>
#wave-wrapper {
  margin: 0;
  padding: 1rem;
  position: relative;

  h4#songtitle {
    margin-bottom: 1.5rem;
  }

  #controller {
    margin: 1rem auto;
    button {
      display: inline-block;
      box-sizing: border-box;
      padding: .5rem;
      margin: 0;
      font-size: 1.25rem;
      background-color: transparent;
      border: 1px solid $text-dark;
      color: $text-black;
    }
  }

  #songlist {

    .song-row {
      display: flex;
      padding: .5rem;
      margin: 0 -0.5rem;
      cursor: pointer;
      align-items: center;

      > * {
        display: inline-block;
      }
      .songnum {
        margin-right: .5rem;
      }
      .songname {
        flex: 1 1 auto;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .download {
        padding: .25rem .5rem;
        font-size: 1.2rem;
        border: 1px solid transparent;
        border-radius: .25rem;
        &:hover {
          border-color: $text-dark;
        }
      }
      .songtime {
        width: 3rem;
        text-align: center;
      }
    }
  }

  #wavetimeline{
    position: relative;
    display: block;
    background-color: rgba(255,255,255,0.3);
  }
  #waveloading{
    position: absolute;
  }
  #timedisplay{
    position: absolute;
    height: 18px;
    width: 110px;
    line-height: 16px;
    padding: 1px 2px;
    margin: 110px 0 0 auto;
    text-align: center;
    font-size: 16px;
    background-color: #333;
    color: #eee;
    z-index: 8;
  }
}
</style>
