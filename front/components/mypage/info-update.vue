<template>
  <div>
    <h3>登録情報変更</h3>
  <section>
    <p class="small my-2">
      メールアドレス関係の設定は
      <router-link to="/mypage/mail-settings/">こちら</router-link>
      に移行しました
    </p>

    <form>
      <div class="form-group">
        <label for="id_last_name">名字:</label>
        <input
          type="text"
          name="last_name"
          v-model="formData.last_name"
          maxlength="255"
          class="form-control"
          required=""
          id="id_last_name">
      </div>
        
      <div class="form-group">
        <label for="id_first_name">名前:</label>
        <input
          type="text"
          name="first_name"
          v-model="formData.first_name"
          maxlength="255"
          class="form-control"
          required=""
          id="id_first_name">
      </div>
        
      <div class="form-group">
        <label for="id_furigana">ふりがな:</label>
        <input
          type="text"
          name="furigana"
          v-model="formData.furigana"
          maxlength="255"
          class="form-control"
          required=""
          id="id_furigana">
      </div>

      <div class="form-group">
        <label for="id_nickname">ニックネーム:</label>
        <input
          type="text"
          name="nickname"
          v-model="formData.nickname"
          maxlength="255"
          class="form-control"
          id="id_nickname">
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
  name: 'mypage-info-update',
  components: {
    nowloading
  },
  metaInfo: {
    title: '登録情報変更'
  },
  created() {
    this.nowloading = true;
    this.$store.dispatch('members/getUserInfo')
    .then(() => {
      this.nowloading = false;
      this.$set(this.formData, "last_name", this.userInfo.last_name);
      this.$set(this.formData, "first_name", this.userInfo.first_name);
      this.$set(this.formData, "furigana", this.userInfo.furigana);
      this.$set(this.formData, "nickname", this.userInfo.nickname);
    })
    .catch(error => {
      nowloading = false;
      console.log(error)
    })
  },
  data: () => ({
    nowloading: false,
    formData: {
      last_name: "",
      first_name: "",
      furigana: "",
      nickname: "",
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
      this.axios.post('/mypage/api/info-update/', this.formData)
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
        this.$store.dispatch('members/getUserInfo');
        this.nowloading = false;
      })
    }
  }
}
</script>