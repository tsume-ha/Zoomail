<template>
  <abstract-content
    :id="id"
    :dataList="lives"
    :oneContentAPIPath="apiPath"
    @setContent="setContent"
  >
    <template #header>
      <abstract-content-header :path="{name: 'sound:index'}" :text="content.title"/>
    </template>
    <player :songs="content.songs" />
  </abstract-content>
</template>

<script>
import AbstractContent from "../../components/AbstractContent.vue";
import AbstractContentHeader from "../../components/AbstractContentHeader.vue";
import Player from "./components/player.vue";
import { useStore } from "vuex";
import { computed, ref } from "vue";
export default {
  components: {
    AbstractContent,
    AbstractContentHeader,
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