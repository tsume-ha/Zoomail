<template>
  <div>
    <h3>メール受信テスト</h3>
  <section>
    <div class="mt-4 mb-2">
      <span class="mb-2">現在設定されているメールアドレス</span>
      <br>
      <span v-if="showEmailAddress">
        {{userInfo.receive_email}}
      </span>
      <span v-else>
        ******************
      </span>
    </div>
    
    <div class="mb-3">
      <button
        v-if="showEmailAddress"
        @click="showEmailAddress=false"
        class="btn btn-sm btn-light"
        >メールアドレスを隠す</button>
      <button
        v-else
        @click="showEmailAddress=true"
        class="btn btn-sm btn-light"
        >メールアドレスを表示する</button>
    </div>

    <p class="small">
      メーリスがきちんと受信できるか確かめるために、テストメールを送信します。<br>
      テストメールの送信は5分に1回行うことができます。
    </p>

    <router-link to="../"  class="btn btn-secondary mx-2 my-3">戻る</router-link>
    <button @click.prevent="onclicked" class="btn btn-info mx-2 my-3">
      送信する
    </button>

  </section>
  <nowloading v-if="nowloading" text="通信中です..." />
  </div>
</template>

<script>
import nowloading from '../nowloading.vue';
export default {
  name: 'mypage-mail-test',
  components: {
    nowloading
  },
  metaInfo: {
    title: 'メール受信テスト'
  },
  created() {
    this.$store.dispatch('members/getUserInfo')
  },
  data: () => ({
    nowloading: false,
    showEmailAddress: false,
  }),
  computed: {
    userInfo () {
      return this.$store.state.members.user;
    }
  },
  methods: {
    onclicked () {
      if (!window.confirm('送信しますか？')) {return false;}
      this.nowloading = true;
      this.axios.post('/mypage/api/mail-test/', {send: "true"})
      .then(res => {
        console.log(res)
        this.$toast.success('送信しました');
      })
      .catch(error => {
        console.log(error)
        if (error.response.status == 400) {
          this.$toast.error(
            "送信できませんでした。通信環境を確認してもう一度試してみてください。",
            {duration: 5000}
            );
        } else if (error.response.status == 429) {
          this.$toast.warning(
            "送信は5分に1回のみ可能です。時間をおいて再度アクセスしてください。",
            {duration: 5000}
            );
        }
      })
      .finally(() => {
        this.nowloading = false;
      })
    }
  }
}
</script>