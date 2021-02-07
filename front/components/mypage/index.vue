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
  })
}
</script>
