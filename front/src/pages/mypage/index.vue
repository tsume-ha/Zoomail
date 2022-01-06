<template>
  <article>
    <h3>My Page</h3>
    <p>メーリスにおける各種設定のページです</p>
    <div class="pure-g">

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <div class="card">
        <h4 class="pure-menu-heading border-info">登録情報</h4>
        <ul class="pure-menu-list">
          <li class="pure-menu-item">
            <router-link :to="{name: 'mypage:profile'}" class="pure-menu-link">
              登録情報変更
            </router-link>
          </li>
          <li class="pure-menu-item">
            <router-link :to="{name: 'mypage:mail-settings'}" class="pure-menu-link">
              メーリス受信設定
            </router-link>
          </li>
          <li class="pure-menu-item">
            <router-link :to="{name: 'mypage:mail-test'}" class="pure-menu-link">
              メーリス受信テスト
            </router-link>
          </li>
          <li class="pure-menu-item">
            <router-link :to="{name: 'mypage:oauth'}" class="pure-menu-link">
              LiveLog・Google認証
            </router-link>
          </li>
        </ul>
        </div>
      </section>

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <div class="card">
        <h4 class="pure-menu-heading border-dark">ログアウト</h4>
        <ul class="pure-menu-list">
          <li class="pure-menu-item">
            <a href="/logout/" class="pure-menu-link">ログアウトする</a>
          </li>
        </ul>
        </div>
      </section>

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <div class="card">
        <h4 class="pure-menu-heading border-warining">ユーザー招待</h4>
        <ul class="pure-menu-list">
          <li class="pure-menu-item">
            <router-link :to="{name: 'mypage:invite'}" class="pure-menu-link">
              招待用フォーム
            </router-link>
          </li>
        </ul>
        </div>
      </section>

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <div class="card">
        <h4 class="pure-menu-heading border-danger">管理サイト</h4>
        <ul class="pure-menu-list">
          <li class="pure-menu-item">
            <a href="/admin/" class="pure-menu-link" target="_blank">Zoomail 管理者用サイト</a>
          </li>
        </ul>
        </div>
      </section>

    </div>
  </article>
</template>

<script>
import { onMounted, reactive } from "vue";
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const permissions = reactive({
      canRegisterUser: false,
      canEnterAdmin: false
    });

    const permissionsUpdate = () => {
      const userData = store.state.user;
      if (userData.is_staff) {
        permissions.canEnterAdmin = true;
      } else {
        permissions.canEnterAdmin = false;
      }
    };
    onMounted(() => permissionsUpdate());

    return {
      permissions
    };
  },
};
</script>

<style lang="scss" scoped>
div.pure-g {
  section.pure-menu-custom {
    div.card {
      padding: 1rem 1rem 1rem 0.75rem;
}}}

.border-info {
  border-color: $bg-info-dark;
}
.border-dark {
  border-color: $bg-secondary-dark;
}
.border-warining {
  border-color: $bg-warining-dark;
}
.border-danger {
  border-color: $text-red;
}
</style>