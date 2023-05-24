<template>
  <article>
    <h3>メーリス・受信ボックス</h3>
    <search-form />

    <div v-if="messages.length === 0 && nowLoading">now loading</div>
    <transition-group name="message-row" v-else appear>
      <one-message-row
        v-for="mes in messages"
        :key="mes.id"
        :message="mes"
        class="one-message-row"
      />
    </transition-group>

    <Paginator :pages="totalPages" :page="page" @pageTo="handlePageJump" />
  </article>
</template>

<script>
import { computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import oneMessageRow from "./components/one-message-row.vue";
import searchForm from "./components/search-form.vue";
import Paginator from "@/components/Paginator.vue";
export default {
  components: {
    oneMessageRow,
    searchForm,
    Paginator,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();

    watch(route, () => {
      if (route.path === "/mail/") {
        updateMessage();
      }
    });

    const messages = computed(() => store.state.read.messages);
    const nowLoading = computed(() => store.state.read.nowLoading);
    const query = computed(() => store.state.read.params);

    const cleanQuery = computed(() => {
      const query = {};
      if (route.query.is_kaisei && route.query.is_kaisei === "true") {
        query.is_kaisei = true;
      }
      if (route.query.is_zenkai && route.query.is_zenkai === "true") {
        query.is_zenkai = true;
      }
      if (route.query.is_bookmark && route.query.is_bookmark === "true") {
        query.is_bookmark = true;
      }
      if (route.query.is_sender && route.query.is_sender === "true") {
        query.is_sender = true;
      }
      if (route.query.text) {
        query.text = route.query.text;
      }
      if (route.query.page && Number(route.query.page) > 1) {
        query.page = Number(route.query.page);
      }
      return query;
    });

    const differentPageQuery = (pageNum) => {
      return {
        ...cleanQuery.value,
        page: pageNum,
      };
    };

    const updateMessage = () => {
      if (
        messages.value.length === 0 ||
        cleanQuery.value.is_kaisei !== query.value.is_kaisei ||
        cleanQuery.value.is_zenkai !== query.value.is_zenkai ||
        cleanQuery.value.is_bookmark !== query.value.is_bookmark ||
        cleanQuery.value.is_sender !== query.value.is_sender ||
        cleanQuery.value.text !== query.value.text ||
        cleanQuery.value.page !== query.value.page
      ) {
        store.dispatch("read/getMessagesFromAPI", cleanQuery.value);
      }
    };

    onMounted(() => updateMessage());

    // pagination
    const page = computed(() => Number(route.query.page) || 1);
    const totalPages = computed(() => store.state.read.totalPages);
    const handlePageJump = (pageTo) => {
      router.push({ query: differentPageQuery(pageTo) });
    };
    return {
      messages,
      nowLoading,
      page,
      totalPages,
      differentPageQuery,
      handlePageJump,
    };
  },
};
</script>

<style scoped>
.one-message-row {
  display: block;
}
.message-row-enter-from,
.message-row-leave-to {
  opacity: 0;
}
.message-row-enter-active {
  transition: all 0.5s;
}
</style>