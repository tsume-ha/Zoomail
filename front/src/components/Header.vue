<template>
  <header>
    <router-link to="/">Zoomail ✉</router-link>
    <NavSW :status="navStatus" @navSWClicked="navSWClicked" />
  </header>
</template>

<script>
import NavSW from "@/components/NavSW.vue";
import { ref } from "vue";
export default {
  components: {
    NavSW,
  },
  setup() {
    const navStatus = ref("toMenu");
    const navSWClicked = () => {
      if (navStatus.value === "toMenu") {
        navStatus.value = "toClose";
      } else if (navStatus.value === "toClose") {
        navStatus.value = "toMenu";
      } else if (navStatus.value === "toReturn") {
        //
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
header {
  display: flex;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
  height: 3rem;
  padding: 0 0.5rem;

  a,
  button {
    flex: auto 0 0;
    align-self: center;
  }
}
</style>