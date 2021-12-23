<template>
  <abstract-content
    :id="id"
    :dataList="lives"
    :oneContentAPIPath="apiPath"
    @setContent="setContent"
  >
    <h3>{{ content.title }}</h3>
    <Player :songs="content.songs" />
  </abstract-content>
</template>

<script>
import AbstractContent from "../../components/AbstractContent.vue";
import Player from "./components/Player.vue";
import { useStore } from "vuex";
import { computed, ref } from "vue";
export default {
  components: {
    AbstractContent,
    Player
  },
  props: {
    id: {required: true, type: Number}
  },
  setup(props) {
    const store = useStore();
    const lives = computed(() => store.state.sound.lives);
    const apiPath = computed(() => `/api/sound/${props.id}/`);

    const content = ref({});
    const setContent = item => {
      content.value = item;
    };

    return {
      lives, apiPath, content, 
      setContent
    };
  },
};
</script>