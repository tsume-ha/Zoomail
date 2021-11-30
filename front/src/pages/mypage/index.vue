<template>
  <main>
    <section>
      <h4>登録情報</h4>
      <router-link :to="{name: 'mypage:profile'}">登録情報変更</router-link>
      <router-link :to="{name: 'mypage:mail-settings'}">メーリス受信設定</router-link>
      <router-link :to="{name: 'mypage:mail-test'}">メーリス受信テスト</router-link>
      <router-link :to="{name: 'mypage:oauth'}">LiveLog・Google認証</router-link>
    </section>
    <section>
      <h4>ログアウト</h4>
      <router-link to="/">ログアウトする</router-link>
    </section>
    <section v-if="permissions.canRegisterUser">
      <h4>ユーザー登録</h4>
      <router-link to="/">ユーザー登録フォーム</router-link>
    </section>
    <section v-if="permissions.canEnterAdmin">
      <h4>管理サイト</h4>
      <a href="/admin/">Zoomail 管理者用サイト</a>
    </section>
  </main>
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