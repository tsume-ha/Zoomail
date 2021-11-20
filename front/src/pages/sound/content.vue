<template>
  <abstract-content
    :id="id"
    :dataList="lives"
    :oneContentAPIPath="apiPath"
    @setContent="setContent"
  >
    <template #header>
      <abstract-content-header :text="content.title"/>
    </template>
    <div>content example</div>
  
  </abstract-content>
</template>

<script>
import AbstractContent from "../../components/AbstractContent.vue"
import AbstractContentHeader from "../../components/AbstractContentHeader.vue"
import { useStore } from "vuex"
import { computed, ref } from '@vue/reactivity';
export default {
  components: {
    AbstractContent,
    AbstractContentHeader
  },
  props: {
    id: {required: true, type: Number}
  },
  setup(props) {
    const store = useStore();
    const lives = computed(() => store.state.sound.lives)
    const apiPath = computed(() => `/api/sound/${props.id}/`)

    const content = ref({});
    const setContent = item => {
      content.value = item;
    }

    return {
      lives, apiPath, content, 
      setContent
    }
  },
}
</script>