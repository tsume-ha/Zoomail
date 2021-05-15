<template>
<div>

  <input type="checkbox" id="nav_open">
  <header>
    <div class="container">
      <h1><a href="/">Zoomail</a></h1>
      <label id="nav_SW" for="nav_open"><span></span></label>
      <nav id="nav">
        <ul>
          <li><router-link to="/read/">メーリス</router-link></li>
          <li><a href="/kansou/">感想用紙</a></li>
          <li><a href="/sound/">リハ音源</a></li>
          <li><a href="/movie/">ライブ映像</a></li>
          <li><a href="/pictures/">写真</a></li>
          <li><a href="/meeting_room/">例会教室</a></li>
          <li><a href="/others/">その他資料</a></li>
          <li><router-link to="/mypage/">My Page</router-link></li>
          <li><a href="/howto/">使い方</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <div class="container my-3">
  <router-view></router-view>
  </div>

</div>
</template>

<script>
  export default {
    name: 'App',
    metaInfo: {
      titleTemplate: chunk => (
          chunk ? `${chunk} | Zoomail` : 'Zoomail'
        )
      }
  }
</script>