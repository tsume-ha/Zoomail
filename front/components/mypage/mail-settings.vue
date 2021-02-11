<template>
  <div>
    <h3>メーリス受信設定</h3>
  <section>
    <form>
      <div class="form-group">
        <label for="id_last_name">受信用メールアドレス:</label>
        <input
          type="email"
          name="last_name"
          v-model="formData.receive_email"
          maxlength="254"
          class="form-control"
          required="false"
          id="id_last_name"
          >
        <p class="small text-secondary">
          メーリスを受信するメールアドレスを指定してください。<br>
          空白の場合は、ログインに用いるGmailアドレスか、
          LiveLogアカウントに登録されたメールアドレスになります。
        </p>
      </div>
      <div class="form-group">
        <label for="id_send_mail" class="">メーリスを受信する:</label>
        <input
          type="checkbox"
          name="send_mail"
          v-model="formData.send_mail"
          class="mx-2"
          id="id_send_mail"
        >
        <p class="small text-secondary">
            メーリスを受け取りたくない場合はチェックを外してください。<br>
            チェックが外されると、全回・回生メーリスともに送信されないようになりますが、<br>
            このサイトにログインし、メーリスを確認することは出来ます。
        </p>
      </div>

      <router-link to="../"  class="btn btn-secondary mx-2 my-3">戻る</router-link>
      <button @click.prevent="onclicked" class="btn btn-info mx-2 my-3">
        更新
      </button>
    </form>

  </section>
  <nowloading v-if="nowloading" text="通信中です..." />
  </div>
</template>

<script>
import nowloading from '../nowloading.vue';
export default {
  name: 'mypage-mail-settings',
  components: {
    nowloading
  },
  metaInfo: {
    title: 'メーリス受信設定'
  },
  created() {
    this.nowloading = true;
    this.$store.dispatch('members/getUserInfo')
    .then(() => {
      this.nowloading = false;
      this.$set(this.formData, "receive_email", this.userInfo.receive_email);
      this.$set(this.formData, "send_mail", this.userInfo.send_mail);
    })
    .catch(error => {
      nowloading = false;
      console.log(error)
    })
  },
  data: () => ({
    nowloading: false,
    formData: {
      receive_email: "",
      send_mail: true,
    }
  }),
  computed: {
    userInfo () {
      return this.$store.state.members.user;
    }
  },
  methods: {
    onclicked () {
      this.nowloading = true;
      this.axios.post('/api/mypage/mail-settings/', this.formData)
      .then(res => {
        if (res.data.successed === true) {
          this.$toast.success('更新しました');
        } else {
          for (const message of res.data.messages) {
            this.$toast.error(message, {duration: 5000});
          }
        }
      })
      .finally(() => {
        this.$store.dispatch('members/getUserInfo')
        .then(() => {
          this.nowloading = false;
          this.$set(this.formData, "receive_email", this.userInfo.receive_email);
          this.$set(this.formData, "send_mail", this.userInfo.send_mail);
        });
      })
    }
  }
}
</script>