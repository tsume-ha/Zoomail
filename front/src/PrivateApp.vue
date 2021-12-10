<template>
  <Header @navSWClicked="navSWClicked" :status="navStatus" />
  <main class="container">
    <transition name="nav-transition">
      <Navigation v-if="navStatus === 'menuOpened'" />
    </transition>
    <router-view />
  </main>
  <Footer />
  <Message />
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import Navigation from "@/components/Navigation.vue";
import Message from "@/components/Message";
export default {
  components: {
    Header,
    Footer,
    Navigation,
    Message,
  },
  setup() {
    const store = useStore();
    store.dispatch("mypage/getUserInfo");

    const navStatus = computed(() => store.state.menuStatus);
    const navSWClicked = () => {
      if (navStatus.value === "menuClosed") {
        store.commit("setMenuStatus", "menuOpened");
      } else if (navStatus.value === "menuOpened") {
        store.commit("setMenuStatus", "menuClosed");
      } else if (navStatus.value === "detail") {
        // return to base
      }
    };

    return {
      navStatus,
      navSWClicked,
    };
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
nav {
  &.nav-transition-enter-active,
  &.nav-transition-leave-active {
    transition: opacity 0.25s;
  }
  &.nav-transition-enter-from,
  &.nav-transition-leave-to {
    opacity: 0;
  }
}
</style>
