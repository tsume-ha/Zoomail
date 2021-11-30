<template>
  <div>
    <h1>index</h1>
    text{{counter}}
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import axios from "../../utils/axios";
export default {
  setup(props) {
    const counter = ref(0);
    console.log(props);
    const store = useStore();

    const content_log = ref([]);
    const announcements = ref([]);
    onMounted(() => {
      axios.get("/api/home/index/").then(res => {
        console.log(res.data);
        content_log.value = res.data.content_log;
        announcements.value = res.data.announcements;
      }).catch(err => {
        store.commit("message/addMessage", {
          level: "error",
          message: String(err.response.status) + " " +  err.response.statusText,
          appname: "index/index"
        });
        console.error(err.response);
      });
    });

    return{
      counter,
      content_log,
      announcements
    };
  }
};
</script>