<template>
  <nav class="container">
    <ul>
      <li>
        <router-link :to="{ name: 'mail:index' }"> メーリス </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'mail:send' }"> メーリス送信 </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'sound:index' }"> リハ音源 </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'movie:index' }"> ライブ映像 </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'photo:index' }"> 写真 </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'kansou:index' }"> 感想用紙 </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'meeting_room:index' }">
          例会教室
        </router-link>
      </li>
      <li>
        <router-link :to="{ name: 'others:index' }"> その他資料 </router-link>
      </li>
      <hr />
      <li>
        <router-link :to="{ name: 'mypage:index' }"> My Page </router-link>
      </li>
      <li>
        <a href="/howto/">使い方</a>
      </li>
    </ul>
  </nav>
</template>
<style lang="scss" scoped>
nav {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  // min-height: calc(100vh - 3rem);
  min-height: 100%;
  z-index: 3;
  text-align: center;
  background-color: $bg-dark;
  color: $text-white;

  ul {
    border-top: 1px solid $text-white;
    padding: 1.25rem 0 3rem;
    margin: 0;

    li {
      display: block;
      list-style: none;
      padding: 1rem;
      margin: 0;
      a {
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        &:hover {
          background-color: $bg-dark-hover;
        }
      }
    }
    hr {
      max-width: 14rem;
      // background-color: $text-white;
      // border-top: 1px dotted $text-white;
      border-width: 1px 0 0 0;
      border-style: solid;
      border-color: $text-white;
    }
  }
}
</style>