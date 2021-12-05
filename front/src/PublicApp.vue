<template>
  <div id="bg-wraper" :class="{'menuOpen': isMenuOpen, 'menuClose': !isMenuOpen}">
    <Header @navSWClicked="navSWClicked" :status="navStatus" />
    <main class="container content-wraper">
      <router-view />
    </main>

    <Footer />
  </div>
</template>


<script>
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
export default {
  components: {
    Header,
    Footer,
  },
  setup() {
    const router = useRouter();
    const store = useStore();

    const navStatus = ref("toMenu");
    const navSWClicked = () => {
      if (navStatus.value === "toMenu") {
        router.push({name: "login"});
      } else if (navStatus.value === "toClose") {
        router.push({name: "index"});
      }
    };
    const isMenuOpen = computed(() => store.state.isMenuOpen);
    watch(
      () => isMenuOpen.value,// target
      (val, _) => {// new, old => {}
        if (val) {
          navStatus.value = "toClose";
        } else {
          navStatus.value = "toMenu";
        }
      }
    );
    return {
      navStatus, isMenuOpen,
      navSWClicked
    };
  },
};
</script>

<style lang="scss">
header, footer {
  background-color: transparent!important;
}
div#bg-wraper {
  min-height: 100vh;
  color: $text-white;
  transition: background 0.5s;
  &.menuOpen {
    background-color: $bg-dark;
  }
  &.menuClose {
    background-color: $bg-light;
  }
}
</style>