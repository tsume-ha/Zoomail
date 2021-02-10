<template>
<div>
  <h3>My Page</h3>
  <p class="col-12 mb-3 mx-0 px-0">
    このページでは、メーリスにおける各種設定が変更できます
  </p>

  <div class="row px-2">
    <menulist
    v-for="item in menuList"
    :key="item.header.text"
    :border-color-class="item.borderColorClass"
    :header="item.header"
    :menu="item.menu"
    />
    <menulist
    v-if="registerMenu"
    :key="registerMenu.header.text"
    :border-color-class="registerMenu.borderColorClass"
    :header="registerMenu.header"
    :menu="registerMenu.menu"
    />
    <menulist
    v-if="canAdminDisplay"
    :key="adminMenu.header.text"
    :border-color-class="adminMenu.borderColorClass"
    :header="adminMenu.header"
    :menu="adminMenu.menu"
    />
  </div>

</div>
</template>

<script>
import menulist from "./menulist.vue";
export default {
  name: 'mypage-index',
  components: {
    menulist
  },
  data: () => ({
    menuList: [
      {
        borderColorClass: 'info',
        header: {text: '登録情報'},
        menu: [
          {text: '登録情報変更', path: './info-update/'},
          {text: 'メーリス受信設定', path: './mail-settings/'},
          {text: 'メーリス受信テスト', path: './mail-test/'},
          {text: 'LiveLog・Google認証', path: './oauth/'},
        ]
      },
      {
        borderColorClass: 'info',
        header: {text: 'メーリス'},
        menu: [
          {text: '送信ボックス', path: './sendbox/'},
        ]
      },
      {
        borderColorClass: 'secondary',
        header: {text: 'ログアウト'},
        menu: [
          {text: 'ログアウトする', path: '/logout/', vueRouter: false},
        ]
      },
    ],
    adminMenu: {
      borderColorClass: 'danger',
      header: {text: '管理サイト'},
      menu: [
        {text: 'DB管理サイト', path: '/admin/', vueRouter: false},
      ]
    },
    registerMenu: {
      borderColorClass: 'warning',
      header: {text: 'ユーザー登録'},
      menu: [
        {text: 'ユーザー登録フォーム', path: './'},
      ]
    }
  }),
  created () {
    this.$store.dispatch('members/getUserInfo')
  },
  computed: {
    user () {
      return this.$store.state.members.user;
    },
    canAdminDisplay () {
      if (this.user && this.user.permissions){
        if (
          this.user.permissions.is_admin
          || this.user.permissions.is_superuser) {
          return true;
        }
      }
      return false;
    },
    canRegisterDisplay () {
      if (this.user && this.user.permissions){
        if (
          this.user.permissions.can_register_user
          || this.user.permissions.is_superuser) {
          return true;
        }
      }
      return false;
    },
  }
}
</script>
