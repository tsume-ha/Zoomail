<template>
  <article>
    <h2>LOG OUT</h2>

    <p>ログアウトが完了しました。</p>

    <router-link :to="{ name: 'index' }" class="btn-flat">
      トップページへ
    </router-link>
  </article>
</template>

<script>
export default {
  setup() {},
};
</script>

<style lang="scss" scoped>
article {
  color: $text-white;
  text-align: center;
  position: relative;

  h2 {
    margin: 1rem;
    font-size: 1.25rem;
  }
}
</style>