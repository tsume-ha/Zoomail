<template>
  <article>
    <div class="logo-wraper">
      <img id="logo" class="pure-img" src="@/assets/img/zoomail.png" />
    </div>

    <p>
      <span>京都大学を中心に活動する</span
      ><span>アコースティック軽音サークル</span><br />
      <span
        >「<a href="https://ku-unplugged.net" target="_blank"
          >京大アンプラグド</a
        >」</span
      ><span>の部内連絡管理アプリ</span>
    </p>

    <router-link :to="{ name: 'login' }" id="login-button" class="btn-flat"
      >LOG IN</router-link
    >
  </article>
</template>

<style lang="scss" scoped>
article {
  text-align: center;

  p {
    text-shadow: 0 0 0.25rem #000;
    > * {
      display: inline-block;
    }
  }

  .logo-wraper {
    display: block;
    max-width: 400px;
    margin: 1rem auto;
  }
  #login-button {
    margin: 2.5rem;
  }
}
</style>