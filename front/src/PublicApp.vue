<template>
  <div id="bg-wraper" :class="{'menuOpen': isMenuOpen, 'menuClose': !isMenuOpen}">
    <Header @navSWClicked="navSWClicked" :status="navStatus" />
    <main class="container content-wraper">
      <transition mode="out-in" name="transition-router">
        <router-view />
      </transition>
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
div#app {
    background-image: linear-gradient(rgba(56, 100, 113, .8), rgba(56, 100, 113, .8)),
                      url("@/assets/img/LP-BG.jpeg");
    background-repeat: no-repeat;
    background-size: cover;
}
div#bg-wraper {
  min-height: 100vh;
  color: $text-white;
  transition: background-color .5s;

  &.menuOpen {
    background-color: $bg-dark;
  }
  &.menuClose {
    background-color: transparent;
  }
}
// article {
//     transition: opacity 5s;
//   // &.transition-router-enter-active,
//   // &.transition-router-leave-active{
//   // }
//   &.transition-router-enter{
//     opacity: 0;
//   }
//   &.transition-router-leave-to{
//     opacity: 0;
//   }
// }
</style>