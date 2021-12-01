<template>
  <span @click="onClicked">SW</span>
</template>

<script>
export default {
  setup(_, context) {
    const onClicked = () => {
      context.emit("navSWClicked");
    };
    return {
      onClicked
    };
  },
};
</script>