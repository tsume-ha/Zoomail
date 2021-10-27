<template>
  <div v-if="status.loading">
    loading...
  </div>
  <div v-else-if="status.notFound">
    404
  </div>
  <div v-else-if="!status.loading && !status.loaded">
    please retry.
  </div>
  <div v-else-if="status.loaded">
    {{id}} {{message.title}}
  </div>
  <div v-else>
  </div>
</template>

<script>
import { computed, reactive } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
export default {
  setup() {
    const route = useRoute();
    const store = useStore();
    const id = Number(route.params.id);

    const status = reactive({
      loading: true,
      loaded: false,
      notFound: false,
    })

    const message = computed(() => store.state.read.messages.find(item => item.id === id));

    if (message.value) {
      status.loaded = true;
      status.loading = false;
    } else {
      // キャッシュにmessageがなかったとき
      store.dispatch('read/loadOneMessage', id).then(() => {
        status.loading = false;
        status.loaded = true;
      }).catch(error => {
        status.loading = false;
        if (error.message == 'Network Error' && error.response === undefined) {
          console.log('通信エラー');
        } else if (error.response.status === 500) {
          status.loaded = true;
          console.log('500')
        } else if (error.response.status === 403){
          status.loaded = true;
          status.notFound = true;
        } else if (error.response.status === 404){
          status.loaded = true;
          status.notFound = true;
        } else {
          console.log(error.message);
        }
      }).then(() => {
        store.dispatch('read/firstLoadMessage');
      })
    }
    return {
      id, message, status
    }
  },
}
</script>