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
    canUnlink () {
      return this.google && this.livelog;
    }
  },
  methods: {
    onclicked () {
      this.nowloading = true;
      this.axios.post('/mypage/api/google_unlink/', { 'unlink': true })
      .then(res => {
        console.log(res)
      })
      .finally(() => {
        this.$store.dispatch('members/getUserInfo');
        this.nowloading = false;
      })
    }
  }
}
</script>