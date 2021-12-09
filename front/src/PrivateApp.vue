<template>
  <Header :status="navStatus" />
  <main class="container">
    <router-view />
  </main>
  <Footer />
  <Message />
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import Message from "./components/message";
export default {
  components: {
    Header,
    Footer,
    Message
  },
  setup() {
    const store = useStore();
    onMounted(store.dispatch("mypage/getUserInfo"));

    const navStatus = ref("toMenu");
    return {
      navStatus
    };
  }
};
</script>
<style lang="scss" scoped>
main{
  background-color: $bg-light;
  > article {
    color: $text-black;
  }
}
</style>
