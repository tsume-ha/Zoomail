<template>
  <AbstractSetting>
    <h3>LiveLog・Google認証</h3>
    <p>認証を行ったサービスのアカウントでログインすることが出来ます。</p>
    <section class="pure-g">
      <div
        class="card-wrapper pure-u-1 pure-u-md-1-2 pure-u-ld-1-3"
        id="google"
      >
        <div class="card oauth-card">
          <div class="oauth-card-row">
            <img
              src="@/assets/img/google.png"
              alt="google"
              width="512"
              height="300"
            />
            <span
              v-text="googleOauth2 ? '認証済み' : '未認証'"
              class="badge"
              :class="{ true: googleOauth2, false: !googleOauth2 }"
            />
          </div>
          <div class="oauth-card-row" v-if="googleOauth2">
            <!-- Google認証済み -->
            <button v-if="livelogAuth0" @click="unlink" class="pure-button">
              <!-- Livelogも認証済み -->
              紐付けを解除する
            </button>
            <p v-else>
              <!-- Livelogは認証まえ -->
              紐付けを解除するためには、もう一度LiveLogへログインしてください
            </p>
          </div>
          <div class="oauth-card-row" v-else>
            <a
              href="/auth/login/google-oauth2?next=/mypage/oauth/"
              class="pure-button button-primary"
            >
              認証する
            </a>
          </div>
        </div>
      </div>
      <div
        class="card-wrapper pure-u-1 pure-u-md-1-2 pure-u-ld-1-3"
        id="livelog"
      >
        <div class="card oauth-card">
          <div class="oauth-card-row">
            <img
              src="@/assets/img/livelog.png"
              alt="livelog"
              width="160"
              height="118"
            />
            <span
              v-text="livelogAuth0 ? '認証済み' : '未認証'"
              class="badge"
              :class="{ true: livelogAuth0, false: !livelogAuth0 }"
            />
          </div>
          <div class="oauth-card-row" v-if="!livelogAuth0">
            <a
              href="/auth/login/auth0?next=/mypage/oauth/"
              class="pure-button button-primary"
            >
              認証する
            </a>
          </div>
        </div>
      </div>
    </section>

    <router-link :to="{ name: 'mypage:index' }" class="pure-button return"
      >戻る</router-link
    >
  </AbstractSetting>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import AbstractSetting from "../../components/AbstractSetting.vue";
export default {
  components: {
    AbstractSetting,
  },
  setup() {
    const store = useStore();
    const loading = computed(() => store.state.mypage.loading);
    const livelogAuth0 = computed(
      () => store.state.mypage.userInfo.livelogAuth0
    );
    const googleOauth2 = computed(
      () => store.state.mypage.userInfo.googleOauth2
    );

    const unlink = () => {
      const formData = new FormData();
      formData.append("unlink", true);
      store.dispatch("mypage/post", {
        path: "/api/mypage/google-unlink/",
        formData,
      });
    };
    return {
      loading,
      livelogAuth0,
      googleOauth2,
      unlink,
    };
  },
};
</script>

<style lang="scss" scoped>
.card-wrapper {
  padding: 1rem;

  .oauth-card {
    width: 100%;
    padding: 0.75rem;

    .oauth-card-row {
      display: flex;
      align-items: center;
      margin-bottom: 1rem;

      span.badge {
        display: inline-block;
        padding: 0.5rem;
        margin: 0.125rem 1.5rem;
        border-radius: 0.5rem;

        &.true {
          background-color: $bg-light-lighten3;
        }
        &.false {
          background-color: $bg-secondary-light;
        }
      }
    }
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