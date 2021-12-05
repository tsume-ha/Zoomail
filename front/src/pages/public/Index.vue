<template>
  <article>
    <div class="pure-g">
      <div class="pure-u-1-1">
Logo
      </div>
    </div>

    <router-link :to="{name: 'login'}" id="login-button" class="btn-flat">LOG IN</router-link>

    <p>
      京都大学を中心に活動するアコースティック軽音サークル<br>
      「<a href="https://ku-unplugged.net" target="_blank">京大アンプラグド</a>」の部内連絡管理アプリ
    </p>

  </article>
</template>

<style lang="scss" scoped>
article{
  text-align: center;

  p {
    text-shadow: 0 0 0.25rem #000;
  }
}
</style>