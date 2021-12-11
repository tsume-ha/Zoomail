<template>
  <article>
    <h4>LOG OUT</h4>

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

  h4 {
    margin: 1rem;
  }
}
</style>