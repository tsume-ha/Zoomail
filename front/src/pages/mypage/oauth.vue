<template>
  <abstract-setting :loading="loading">
    <section>
      <p>認証を行ったサービスのアカウントでログインすることが出来ます。</p>
      <table class="table">
        <tbody>
          <tr>
            <td>Google</td>
            <td>
              <span v-if="googleOauth2" class="text-success">認証しています</span>
              <a v-else href="/auth/login/google-oauth2?next=/mypage/oauth/">認証する</a>
            </td>
            <td v-if="googleOauth2 && livelogAuth0">
              <a @click="unlink" class="text-warning">紐付けを解除する</a>
            </td>
            <td v-else>
              <span>紐付けを解除するまえに、もう一度LiveLogへログインしてください</span>
            </td>
          </tr>
          <tr>
            <td>LiveLog</td>
            <td>
              <span v-if="livelogAuth0" class="text-success">認証しています</span>
              <a v-else href="/auth/login/auth0?next=/mypage/oauth/">
                認証する
              </a>
            </td>
            <td v-if="googleOauth2 && livelogAuth0"></td>
            <td v-else>
              <a href="/auth/login/auth0?next=/mypage/oauth/">
                LiveLogにログイン
              </a>
            </td>
          </tr>
        </tbody>
      </table>
      <router-link :to="{name: 'mypage:index'}" class="btn btn-secondary mr-4">戻る</router-link>
    </section>
  </abstract-setting>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import AbstractSetting from "../../components/AbstractSetting.vue";
export default {
  components: {
    AbstractSetting
  },
  setup() {
    const store = useStore();
    const loading = computed(() => store.state.mypage.loading);
    const livelogAuth0 = computed(() => store.state.mypage.userInfo.livelogAuth0);
    const googleOauth2 = computed(() => store.state.mypage.userInfo.googleOauth2);
    
    const unlink = () => {
      const formData = new FormData();
      formData.append("unlink", true)
      store.dispatch("mypage/post", {path: "/api/mypage/google-unlink/", formData});
    }
    return {
      loading, livelogAuth0, googleOauth2,
      unlink
    }
  }
}
</script>