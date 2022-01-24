<template>
  <article>
    <slot />
    <Loading
      v-model:active="loading"
      :can-cancel="false"
      :is-full-page="true"
      color="#386471"
    />
  </article>
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

const store = useStore();

const loading = computed(() => store.state.mypage.loading);
</script>
