<template>
  <article>
    <div class="logo-wraper">
      <img id="logo" class="pure-img" src="@/assets/img/zoomail.png">
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

  .logo-wraper {
    display: block;
    max-width: 400px;
    margin: 1rem auto 2rem;
  }
}
</style>