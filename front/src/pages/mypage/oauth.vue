<template>
  <abstract-setting :loading="loading">
    <h3>LiveLog・Google認証</h3>
    <p>認証を行ったサービスのアカウントでログインすることが出来ます。</p>
    <section class="pure-g">
      <div class="card-wrapper pure-u-1 pure-u-md-1-2 pure-u-ld-1-3" id="google">
        <div class="card oauth-card">
          <div class="oauth-card-row">
            <img src="@/assets/img/google.png" alt="google" width="512" height="300">
            <span class="badge" v-text="googleOauth2 ? '認証済み' : '未認証'" />
          </div>
          <a href="/auth/login/google-oauth2?next=/mypage/oauth/">認証する</a>
        </div>
      </div>
      <div class="card-wrapper pure-u-1 pure-u-md-1-2 pure-u-ld-1-3" id="livelog">
        <div class="card oauth-card">
          <img src="@/assets/img/livelog.png" alt="livelog" width="160" height="118" />
          <a href="/auth/login/auth0?next=/mypage/oauth/">認証する</a>
        </div>
      </div>
    </section>

    <router-link :to="{name: 'mypage:index'}" class="pure-button">戻る</router-link>
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
      formData.append("unlink", true);
      store.dispatch("mypage/post", {path: "/api/mypage/google-unlink/", formData});
    };
    return {
      loading, livelogAuth0, googleOauth2,
      unlink
    };
  }
};
</script>

<style lang="scss" scoped>
.card-wrapper {
  padding: 1rem;

  .oauth-card {
    width: 100%;
    padding: .75rem;
  }
}

#livelog {
  img {
    height: 3rem;
    width: auto;
  }
}
#google {
  img {
    height: 3rem;
    width: auto;
  }
}
</style>