<template>
  <div v-if="status.loading">
    loading...
  </div>
  <div v-else-if="status.notFound">
    404
  </div>
  <div v-else-if="!status.loading && !status.loaded">
    please retry.
    <button @click="reload">再読み込み</button>
  </div>
  <div v-else-if="status.loaded">
    <slot name="header" />
    <slot />
  </div>
  <div v-else>
  </div>
</template>

<script>
import { reactive } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import axios from "../utils/axios";
export default {
  props: {
    id: {type: Number, required: true},
    dataList: {type: Array, required: true},
    oneContentAPIPath: {type: String, required: true},
  },
  setup(props, context) {
    const route = useRoute();
    const store = useStore();
    const id = Number(route.params.id);

    const status = reactive({
      loading: true,
      loaded: false,
      notFound: false,
    });

    const loadAPI = () => {
      axios.get(props.oneContentAPIPath).then(res => {
        status.loaded = true;
        const item = {...res.data};
        context.emit("setContent", item);
      }).catch(error => {
        if (error.message == 'Network Error' && error.response === undefined) {
          console.log('通信エラー');
        } else if (error.response.status === 500) {
          status.loaded = true;
          console.log('500');
        } else if (error.response.status === 403){
          status.loaded = true;
          status.notFound = true;
        } else if (error.response.status === 404){
          status.loaded = true;
          status.notFound = true;
        } else {
          console.log(error.message);
          store.commit('message/addMessage', {
            level: "error",
            message: "予想外のエラーが帰ってきました。: " + error.message,
            appname: "abscractComtent"
          });
        }
      }).finally(() => {
        status.loading = false;
      });
    };

    if (props.dataList.some(item => Number(item.id) === id)) {
      const item = {...props.dataList.find(item => Number(item.id) === id)};
      context.emit("setContent", item);
      status.loading = false;
      status.loaded = true;
    } else {
      loadAPI();
    }

    const reload = () => loadAPI();

    return {
      status,
      reload
    };
  },
};
</script>