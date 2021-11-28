<template>
  <div v-if="loading">loading</div>
  <div v-else>
    <slot />
  </div>
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
    }
  }
}
</script>
