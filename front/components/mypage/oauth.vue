<template>
  <div>
    <h3>LiveLog・Google認証</h3>
  <section>
    <p>認証を行ったサービスのアカウントでログインすることが出来ます。</p>
    <table class="table">
      <tbody>
        <tr>
          <td>Google</td>
          <td>
            <span v-if="google" class="text-success">認証しています</span>
            <a v-else href="/auth/login/google-oauth2?next=/mypage/oauth/">認証する</a>
          </td>
          <td v-if="canUnlink">
            <a @click="onclicked" class="text-warning">紐付けを解除する</a>
          </td>
          <td v-else-if="needLivelogLogin">
            <span>紐付けを解除するまえに、もう一度LiveLogへログインしてください</span>
          </td>
        </tr>
        <tr>
          <td>LiveLog</td>
          <td>
            <span v-if="livelog" class="text-success">認証しています</span>
            <a v-else href="/auth/login/auth0?next=/mypage/oauth/">
              認証する
            </a>
          </td>
          <td v-if="canUnlink"></td>
          <td v-else-if="needLivelogLogin">
            <a href="/auth/login/auth0?next=/mypage/oauth/">
              LiveLogにログイン
            </a>
          </td>
        </tr>
      </tbody>
    </table>
    <router-link to="../" class="btn btn-secondary mr-4">戻る</router-link>
  </section>
  <nowloading v-if="nowloading" text="通信中です..." />
  </div>
</template>

<script>
import nowloading from '../nowloading.vue';
export default {
  name: 'mypage-oauth',
  metaInfo: {
    title: 'LiveLog・Google認証'
  },
  components: {
    nowloading
  },
  created() {
    this.$store.dispatch('members/getUserInfo');
  },
  data: () => ({
    nowloading: false,
  }),
  computed: {
    userInfo () {
      return this.$store.state.members.user;
    },
    google () {
      return this.userInfo.google_oauth2;
    },
    livelog () {
      return this.userInfo.livelog_auth0;
    },
    hasLivelogEmail () {
      return Boolean(this.userInfo.livelog_email);
    },
    canUnlink () {
      return this.google && this.livelog && this.hasLivelogEmail;
    },
    needLivelogLogin () {
      return this.google && this.livelog && !this.hasLivelogEmail;
    }
  },
  methods: {
    onclicked () {
      this.nowloading = true;
      this.axios.post('/api/mypage/google_unlink/', { 'unlink': true })
      .then(res => {
        if (res.data.deleted) {
          this.$toast.success('Gogleアカウントの紐付けを解除しました');
        } else {
          this.$toast.warning('Gogleアカウントの紐付けを解除ができませんでした。お手数ですが開発者までお問い合わせください');
        }
      })
      .catch(error => {
        console.log(error.response.data)
        if (error.response.data && 'message' in error.response.data){
          this.$toast.error(
            error.response.data['message'],
            {duration: 5000}
            )
        }
        this.$toast.error(
          '処理が完了しませんでした。',
            {duration: 5000}
          )
      })
      .finally(() => {
        this.$store.dispatch('members/getUserInfo');
        this.nowloading = false;
      })
    }
  }
}
</script>