<template>
  <div>
    <h1>mail/read - search</h1>
    <search-form />
    
    <div v-if="nowLoading">now loading</div>
    <transition-group name="message-row" v-else>
      <one-message-row v-for="mes in messages" :key="mes.id" :message="mes" class="one-message-row" />
    </transition-group>

    <router-link :to="{query: differentPageQuery(2)}">Next</router-link>
  </div>
</template>

<script>
import { computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import oneMessageRow from "./components/one-message-row.vue";
import searchForm from "./components/search-form.vue";
export default {
  components: {
    oneMessageRow,
    searchForm
  },
  setup() {
    const store = useStore();
    const route = useRoute();

    watch(route, () => { updateMessage(); });

    const messages = computed(() => store.state.read.messages);
    const nowLoading = computed(() => store.state.read.nowLoading);

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

    const differentPageQuery = pageNum => {
      return {
        ...cleanQuery.value,
        page: pageNum
      };
    };

    const updateMessage = () => {
      store.dispatch(
        "read/getMessagesFromAPI", cleanQuery.value
      );
    };

    if (messages.value.length === 0) {
      updateMessage();
    }
    
    onMounted(() => updateMessage());

    return{
      messages, nowLoading,
      differentPageQuery
    };
  }
};
</script>

<style scoped>
.one-message-row{
  display: block;
}
.message-row-leave-active{
  position: absolute;
}
.message-row-move{
  transition: all 0.5s;
}
/* .message-row-enter-active{
  transition: all 5s;
}
.message-row-enter{
  opacity: 0;
}
.message-row-enter-to{
  opacity: 1;
} */
</style>