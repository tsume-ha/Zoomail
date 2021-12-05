<template>
  <div id="bg-wraper" :class="[navStatus]">
    <Header @navSWClicked="navSWClicked" :status="navStatus" />
    <main class="container content-wraper">
      <router-view />
    </main>

    <Footer />
  </div>
</template>


<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
export default {
  components: {
    Header,
    Footer,
  },
  setup() {
    const router = useRouter();
    const navStatus = ref("toMenu");
    const navSWClicked = () => {
      if (navStatus.value === "toMenu") {
        router.push({name: "login"});
        navStatus.value = "toClose";
      } else if (navStatus.value === "toClose") {
        router.push({name: "index"});
        navStatus.value = "toMenu";
      }
    };
    return {
      navStatus,
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
  &.toClose {
    background-color: $bg-dark;
  }
  &.toMenu {
    background-color: $bg-light;
  }
}
</style>