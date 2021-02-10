<template>
  <div>
    <h3>新規ユーザー登録(Googleアカウント登録)</h3>
    <p>
      LiveLogアカウントの新規登録は初回のログイン時に自動で行われます。
      詳しくは<a href="/howto/introduction/">こちら</a>をご覧ください。
    </p>
    <p>
      Googleアカウントでの一括登録（CSVファイル登録）は
      廃止しました。
    </p>
  <section>
    <form>
      <div class="form-group">
        <label for="id_last_name">Gmailアドレス（Googleアカウント）</label>
        <input
          type="email"
          v-model="formData.email"
          maxlength="254"
          class="form-control"
          required
          >
      </div>

      <div class="form-group">
        <label for="id_last_name">入部年度:</label>
        <input
          type="number"
          name="year"
          v-model="formData.year"
          class="form-control"
          required
          >
      </div>

      <div class="form-group">
        <label for="id_last_name">名字:</label>
        <input
          type="text"
          name="last_name"
          v-model="formData.last_name"
          maxlength="255"
          class="form-control"
          required
          >
      </div>
        
      <div class="form-group">
        <label for="id_first_name">名前:</label>
        <input
          type="text"
          name="first_name"
          v-model="formData.first_name"
          maxlength="255"
          class="form-control"
          required
          >
      </div>
        
      <div class="form-group">
        <label for="id_furigana">ふりがな:</label>
        <input
          type="text"
          name="furigana"
          v-model="formData.furigana"
          maxlength="255"
          class="form-control"
          required
          >
      </div>

      <router-link to="../"  class="btn btn-secondary mx-2 my-3">戻る</router-link>
      <button @click.prevent="onclicked" class="btn btn-warning mx-2 my-3">
        登録する
      </button>
    </form>
    <p>
      登録が完了すると、入力されたGmailアドレスに登録完了の通知が送信されます。
    </p>
  </section>
  <nowloading v-if="nowloading" text="通信中です..." />
  </div>
</template>

<script>
import nowloading from '../nowloading.vue';
export default {
  name: 'mypage-register',
  components: {
    nowloading
  },
  metaInfo: {
    title: '新規ユーザー登録'
  },
  data: () => ({
    nowloading: false,
    formData: {
      email: "",
      year: null,
      last_name: "",
      first_name: "",
      furigana: "",
    }
  }),
  methods: {
    onclicked () {
      if (
           !this.formData.email
        || !this.formData.year
        || !this.formData.last_name
        || !this.formData.first_name
        || !this.formData.furigana
      ) {return false;}
      this.nowloading = true;
      this.axios.post('/mypage/api/register/', this.formData)
      .then(res => {
        if (res.data.successed === true) {
          for (const message of res.data.messages) {
            this.$toast.success(message);
          }
          // form data を初期化
          this.formData = {
            email: "",
            year: null,
            last_name: "",
            first_name: "",
            furigana: "",
          }
        } else {
          for (const message of res.data.messages) {
            this.$toast.error(message, {duration: 5000});
          }
        }
      })
      .catch(error => {
        if (!error.response){
          this.$toast.error("通信に失敗しました。もう一度送信してください。", {duration: 5000});
        } else {
          if (error.response.status == 403){
            this.$toast.error("権限がありません", {duration: 5000});
          }
        }
        this.$toast.error("エラーが発生しました", {duration: 5000});
      })
      .finally(() => {
        this.nowloading = false;
      })
    }
  }
}
</script>