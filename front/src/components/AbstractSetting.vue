<template>
  <article v-if="loading">loading</article>
  <article v-else>
    <slot />
  </article>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();

    const loading = computed(() => store.state.mypage.loading);

    return {
      loading
    };
  }
};
</script>
