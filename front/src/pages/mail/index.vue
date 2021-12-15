<template>
  <article>
    <h3>メーリス・受信ボックス</h3>
    <search-form />
    
    <div v-if="nowLoading">now loading</div>
    <transition-group name="message-row" v-else appear>
      <one-message-row v-for="mes in messages" :key="mes.id" :message="mes" class="one-message-row" />
    </transition-group>

    <!-- <router-link :to="{query: differentPageQuery(2)}">Next</router-link> -->
    <Paginator :pages="30" :page="page" @pageTo="handlePageJump" />
  </article>
</template>

<script>
import { computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, onBeforeRouteLeave, useRouter } from "vue-router";
import oneMessageRow from "./components/one-message-row.vue";
import searchForm from "./components/search-form.vue";
import Paginator from "@/components/Paginator.vue";
export default {
  components: {
    oneMessageRow,
    searchForm,
    Paginator
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();

    watch(route, () => { updateMessage(); });
    onBeforeRouteLeave((_to, _from, next) => {
      updateMessage();
      next();
    });

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


    // pagination
    const page = computed(() => Number(route.query.page));
    const handlePageJump = pageTo => {
      router.push({query: differentPageQuery(pageTo)});
    };
    return{
      messages, nowLoading, page,
      differentPageQuery, handlePageJump
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
  transition: all .5s;
}
.message-row-enter-active{
  transition: all .5s;
}
.message-row-enter-from{
  opacity: 0;
}
.message-row-enter-to{
  opacity: 1;
}
</style>