<template>
  <section id="app">
    <h3>メール受信テスト</h3>
    <p>
      現在設定されている受信メールアドレス：
      <br />
      <span>
        {{ email }}
        <a
          @click="toggleEmailDisplay"
          class="text-primary"
        >{{toggleEmailDisplayNotation}}</a>
      </span>
    </p>
    <p>
      上記のメールアドレスにテストメールを送信します。
      <br />ご自身の受信ボックスを確認し、きちんとメールが受け取れるか、確認してください。
      <br />
      <span class="small">テストメールは、5分に1回送信することが出来ます。</span>
    </p>
    <a href="/members" class="btn btn-secondary mr-4">戻る</a>
    <button @click="send" class="btn btn-info">テストメールを送信する</button>
    <p class="my-3" :class="{'text-danger': isError}">{{ message }}</p>
  </section>
</template>
<script>
export default {
  data: function() {
    return {
      displayEmail: false,
      user: {},
      inProcess: false,
      message: "",
      isError: false
    };
  },
  computed: {
    email: function() {
      if (this.displayEmail) {
        return this.user.receive_email;
      } else {
        return "*********";
      }
    },
    toggleEmailDisplayNotation: function() {
      if (this.displayEmail) {
        return "メールアドレスを隠す";
      } else {
        return "メールアドレスを表示する";
      }
    }
  },
  methods: {
    toggleEmailDisplay: function() {
      this.displayEmail = !this.displayEmail;
    },
    getUser() {
      this.axios.get("/members/api/user").then(res => {
        this.user = Object.create(res.data);
      });
    },
    send: function() {
      if (this.inProcess) {
        return;
      }
      this.inProcess = true;
      this.message = "送信中...";
      this.isError = false;
      let url = window.location.href;

      this.axios
        .post(url, { send: "true" })
        .then(response => {
          this.isError = false;
          this.message = "送信しました！";
        })
        .catch(error => {
          console.log(error);
          this.isError = true;
          if (!error.response) {
            console.log("network error");
            this.message =
              "通信に失敗しました。インターネットへの接続を確認し、再度送信ボタンを押してください。(Network Error)";
          } else if (error.response.status == 429) {
            console.log(error.response.statusText);
            this.message =
              "送信は5分に1回のみ可能です。時間をおいて再度アクセスしてください。(" +
              error.response.status +
              " " +
              error.response.statusText +
              ")";
          } else {
            console.log("internal error");
            this.message =
              "処理に失敗しました。メールが正常に送信されなかった可能性があります。お手数ですが、開発者までご連絡ください。(" +
              error.response.status +
              " " +
              error.response.statusText +
              ")";
          }
        })
        .finally(() => (this.inProcess = false));
    }
  },
  created() {
    this.getUser();
  }
};
</script>
<style type="text/css">
</style>