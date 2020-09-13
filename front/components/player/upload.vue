<template>
<section>
    <template v-if="!states.isPostClicked">
    <h5>1.イベント名、収録日を入力してください。</h5>
    <form id="live-name" class="my-3">
      <label>収録イベント名</label>
      <input
        type="text"
        v-model="livename"
        name="livename"
        placeholder="NFリハ#2"
        class="form-control"
      />
      <label>収録日</label>
      <input
        type="hidden"
        :value="recorded_at"
        name="recorded_at"
        class="form-control"
      />
      <v-date-picker v-model="date" mode="single" :first-day-of-week="2"></v-date-picker>
    </form>
    <h5>2.MP3ファイルを選択してください。</h5>
    <form id="file-select" class="my-3">
      <input type="file" name="songfile" id="songfile" accept="audio/mp3" ref="songfile" @change="onFileChange"
        multiple />
      <label for="songfile" id="input-label">
        ここをクリックしてMP3ファイルを選択してください<br>
        複数選択出来ます<br>
        （ドラッグ＆ドロップには対応していません）
      </label>
    </form>
    <h5>3.トラックナンバーと曲名を確認して送信してください。</h5>
    <div id="show-songs" class="mb-4">
      <template v-if="isFileSelected">
        <div class="row">
          <div class="col-2 col-sm-2 col-md-2">No.</div>
          <div class="col-10 col-sm-8 col-md 7">曲名</div>
        </div>
        <div v-for="file in files" :key="file.name" class="form-row mb-1 song-row">
          <div class="col-2 col-sm-2 col-md-2">
            <input type="number" v-model.number="filenames[file.name].number" class="form-control" />
          </div>
          <div class="col-10 col-sm-8 col-md 7">
            <input type="text" v-model="filenames[file.name].title" class="form-control" />
          </div>
        </div>
        <button class="btn my-3" :class="{
            'btn-info': is_valid,
            'btn-secondary': !is_valid,
          }" :disabled="!is_valid" @click.once="onClick">送信</button>
        <span class="text-warning" v-if="!is_valid">{{errorMessage}}</span>
      </template>
      <template v-else>
        <p>選択されたMP3ファイルがここに表示されます</p>
      </template>
    </div>
  </template>
  <template v-else>
    <h5>4.送信中</h5>
    <template>
      <p class="text-danger" v-if="!states.isComplete">通信が完了するまでページを開いたままにしておいてください。</p>
      <p class="text-success" v-else>送信が完了し、公開されました！</p>
    </template>
    <template>
      <p v-if="states.isError" class="text-danger">
        通信に失敗しました。通信環境を確認し、下の再送信ボタンから再送信してください。<br>
        そのあとに、編集画面に行き正常にデータが反省されているか確認してください。<br>
        <button class="btn btn-warning" @click="POST">再送信</button>
      </p>
    </template>
    <div>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">曲順</th>
            <th scope="col">曲名</th>
            <th scope="col">状態</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in files" :key="item.name">
            <td>{{filenames[item.name].number}}</td>
            <td>{{filenames[item.name].title}}</td>
            <td v-text="process[filenames[item.name].process]" :class="{
              'text-secondary': (filenames[item.name].process == 'yet'),
              'text-primary': (filenames[item.name].process == 'now'),
              'text-success': (filenames[item.name].process == 'done'),
              'text-danger': (filenames[item.name].process == 'error'),
            }"></td>
          </tr>
        </tbody>
      </table>
    </div>
    <a href="/sound/" class="btn btn-success mb-4" v-if="states.isComplete">「音源」トップページに戻る</a>
  </template>
</section>
</template>

<script>
export default {
  data: function () {
    return{
      date: new Date(),
      livename: '',
      files: [],//FileList Object
      filenames: {},//{'01-song.mp3': {'number': 1, 'title': 'song', 'process': 'now'}}
      errorMessage: "",
      process: { 'yet': '準備中', 'now': '送信中', 'done': '完了', 'error': 'エラー' },
      states: {
        isPostClicked: false,
        completeNumber: 0,
        isComplete: false,
        isError: false,
      },
      postUrl: '',
    }
  },
  created: function () {
    this.postUrl = window.location.href;
  },
  methods: {
    onFileChange: function () {
      this.files = this.$refs.songfile.files;
      if (this.files.length == 0) {
        return false;
      }
      for (let file of this.files) {
        let filename = file.name;
        if (this.filenames[filename] !== undefined) {
          continue;
        }
        const spacer = [' ', '-', '_', '.',];
        let indexNum;
        for (var i = 0; i < spacer.length; i++) {
          indexNum = filename.indexOf(spacer[i]);
          if (indexNum < 3) {
            break;
          }
        }
        const trackNumber = Number(filename.slice(0, indexNum));
        const songtitle = filename.slice(indexNum + 1, -4);
        this.$set(this.filenames, filename, { 'number': trackNumber, 'title': songtitle, 'process': 'yet' });
      }
    },
    onClick: function () {
      this.states.isPostClicked = true;
      this.POST();
    },
    POST: function () {
      const file = this.files[this.states.completeNumber]
      const key = file.name;
      this.filenames[key].process = 'now';
      let data = new FormData();
      data.append('file', file);
      data.append('track_num', this.filenames[key].number);
      data.append('song_name', this.filenames[key].title);
      data.append('livename', this.livename);
      data.append('recorded_at', this.recorded_at);
      this.axios
        .post(this.postUrl, data)
        .then(response => {
          this.filenames[key].process = 'done';
          this.states.completeNumber += 1;
          if (this.states.completeNumber < this.files.length) {
            this.POST();
          } else {
            this.states.isComplete = true;
          }
        })
        .catch(error => {
          // エラー時
          this.filenames[key].process = 'error';
          this.states.isError = true;
        });
    }
  },
  computed: {
    isFileSelected: function () {
      return this.files.length > 0;
    },
    recorded_at: function () {
      if (this.date === null) {
        return '';
      } else {
        return this.date.getFullYear() + '-' + ('0' + (this.date.getMonth() + 1)).slice(-2) + '-' + ('0' + this.date.getDate()).slice(-2);
      }
    },
    is_valid: function () {
      // TO DO // ファイルサイズ確認
      if (this.livename.length == 0 || this.livename.length > 255) {
        this.errorMessage = "ライブ名に不正な値が入力されています";
        return false;
      }
      if (this.date == null) {
        this.errorMessage = "収録日を指定してください";
        return false;
      }
      if (!this.isFileSelected) {
        this.errorMessage = "ファイルを選択してください";
        return false;
      }
      for (let key in this.filenames) {
        if (this.filenames[key].title.length == 0 || this.filenames[key].title.length > 500) {
          this.errorMessage = "曲名に不正な値が入力されているものがあります";
          return false;
        }
        if (this.filenames[key].number <= 0 || this.filenames[key].number > 100) {
          this.errorMessage = "曲番号に不正な値が入力されているものがあります";
          return false;
        }
      }
      for (const file of this.files) {
        if (file.size > 20 * 1024 * 1024) {
          this.errorMessage = "ファイルサイズが上限の20MBよりも大きい物があります";
          return false;
        }
      }
      this.errorMessage = "";
      return true;
    }
  }
}
</script>

<style scoped>
form {
  max-width: 800px;
}

#file-select input {
  display: none;
}

#file-select #input-label {
  position: relative;
  display: block;
  margin: 0.5rem 0;
  padding: 1rem;
  width: 100%;
  text-align: center;
  background-color: #f1f9fc;
  border: 2px dotted #d6eef5;
  cursor: pointer;
}

.name input{
  min-width: 240px;
}

.file{
  position: relative;
  margin: 1px;
}

.file input{
  opacity: 0;
  width: 360px;
  z-index: 2;
}
.file span{
  position: absolute;
  left: 5px;
  top: 2px;
  padding: 5px;
  width: 360px;
  background-color: #eee;
}

</style>