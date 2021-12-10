<template>
  <div id="bg-wraper" :class="{ menuOpen: isMenuOpen, menuClose: !isMenuOpen }">
    <Header @navSWClicked="navSWClicked" :status="navStatus" />
    <main class="container content-wraper">
      <router-view v-slot="{ Component }">
        <transition mode="out-in" name="transition-router">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <Footer />
    <Message />
  </div>
</template>


<script>
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import Message from "@/components/Message";
export default {
  components: {
    Header,
    Footer,
    Message,
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const navStatus = ref("menuClosed");
    const navSWClicked = () => {
      if (navStatus.value === "menuClosed") {
        router.push({ name: "login" });
      } else if (navStatus.value === "menuOpened") {
        router.push({ name: "index" });
      }
    };
    const isMenuOpen = computed(() => store.state.isMenuOpen);
    watch(
      () => isMenuOpen.value, // target
      (val, _) => {
        // new, old => {}
        if (val) {
          navStatus.value = "menuOpened";
        } else {
          navStatus.value = "menuClosed";
        }
      }
    );
    return {
      navStatus,
      isMenuOpen,
      navSWClicked,
    };
  },
};
</script>

<style lang="scss">
header,
footer {
  background-color: transparent !important;
}
div#app {
  background-image: linear-gradient(
      rgba(56, 100, 113, 0.8),
      rgba(56, 100, 113, 0.8)
    ),
    url("@/assets/img/LP-BG.jpeg");
  background-repeat: no-repeat;
  background-size: cover;
}
div#bg-wraper {
  min-height: 100vh;
  color: $text-white;
  transition: background-color 0.5s;

  &.menuOpen {
    background-color: $bg-dark;
  }
  &.menuClose {
    background-color: transparent;
  }
}
main > article {
  border-top: 1px solid $text-white;
}
article {
  &.transition-router-enter-active,
  &.transition-router-leave-active {
    transition: opacity 0.1s;
  }
  &.transition-router-enter-from,
  &.transition-router-leave-to {
    opacity: 0;
  }
}
</style>