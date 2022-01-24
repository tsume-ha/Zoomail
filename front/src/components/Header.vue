<template>
  <header class="container">
    <router-link to="/">
      <h1>Zoomail <Icon :icon="['far', 'envelope']" /></h1>
    </router-link>
    <NavSW :status="props.status" @navSWClicked="navSWClicked" />
  </header>
</template>

<script>
import NavSW from "@/components/NavSW.vue";
export default {
  components: {
    NavSW,
  },
  props: {
    status: {
      required: true,
      validator: (value) =>
        ["menuClosed", "menuOpened", "detail"].indexOf(value) !== -1,
    },
  },
  setup(props, context) {
    const navSWClicked = () => {
      context.emit("navSWClicked");
    };
    return {
      props,
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
  color: $text-white;
  background-color: $bg-dark;

  & > * {
    flex: auto 0 0;
    align-self: center;
    margin: 0;
  }
  & h1 {
    height: 30px;
    font-size: 30px;
    line-height: 1;
  }
}
</style>