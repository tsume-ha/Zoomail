<template>
  <footer class="container">
    <span>
      © 2019-2022 京大アンプラグド
    </span>
    <a href="https://twitter.com/ku_unplugged_hp">
      <Icon :icon="['fab', 'twitter']" />
      Twitter
    </a>
    <a href="https://github.com/tsume-ha/Zoomail">
      <Icon :icon="['fab', 'github']" />
      GitHub
    </a>
  </footer>
</template>

<style lang="scss" scoped>
footer {
  display: block;
  background-color: $bg-dark;
  padding-top: 0.5rem;
  color: $text-white;
  font-size: 0.75rem;
  line-height: 1.25;
  text-align: center;
  
  & > * {
    margin-left: 0.5rem;
  }
  a:hover {
    text-decoration: underline;
  }
}
</style>