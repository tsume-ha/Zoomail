<template>
  <Header />
  <div class="container">
    <main>
      <article>
        <router-view />
      </article>
    </main>

    <Footer />
  </div>
</template>


<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
export default {
  components: {
    Header,
    Footer,
  },
  setup() {},
};
</script>

<style lang="scss" scoped>
header {
  background-color: $bg-dark;
}
</style>