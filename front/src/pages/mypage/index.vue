<template>
  <article>
    <h3>My Page</h3>
    <p>メーリスにおける各種設定のページです</p>
    <div class="pure-g">

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <h4 class="pure-menu-heading">登録情報</h4>
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
      </section>

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <h4 class="pure-menu-heading">ログアウト</h4>
        <ul class="pure-menu-list">
          <li class="pure-menu-item">
            <a href="/logout/" class="pure-menu-link">ログアウトする</a>
          </li>
        </ul>
      </section>

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <h4 class="pure-menu-heading">ユーザー登録</h4>
        <ul class="pure-menu-list">
          <li class="pure-menu-item">
            <a href="/" class="pure-menu-link">ユーザー登録フォーム</a>
          </li>
        </ul>
      </section>

      <section class="pure-menu-custom pure-u-1 pure-u-sm-1 pure-u-md-1-2 pure-u-lg-1-3">
        <h4 class="pure-menu-heading">管理サイト</h4>
        <ul class="pure-menu-list">
          <li class="pure-menu-item">
            <a href="/admin/" class="pure-menu-link">Zoomail 管理者用サイト</a>
          </li>
        </ul>
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