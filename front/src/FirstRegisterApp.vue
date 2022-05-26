<template>
  <Header :status="'menuClosed'" />
  <main class="container">
    
    <article>
      hogehoge
    </article>

  </main>
  <Footer />
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
export default {
  components: {
    Header,
    Footer,
  },
};
</script>
<style lang="scss" scoped>
main {
  position: relative;
  background-color: $bg-light;
  > article {
    color: $text-black;
  }
}
</style>
