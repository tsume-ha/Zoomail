<template>
  <abstract-content
    :id="id"
    :dataList="messages"
    :oneContentAPIPath="apiPath"
    @setContent="setMessage"
  >
    <template #header>
      <abstract-content-header :path="{name: 'mail:index'}" :text="message.title"/>
    </template>
    <div>content example</div>
  
  </abstract-content>
</template>

<script>
import AbstractContent from "../../components/AbstractContent.vue";
import AbstractContentHeader from "../../components/AbstractContentHeader.vue";
import { computed, ref } from "vue";
import { useStore } from "vuex";
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
    // for AbstractContent.vue
    const messages = computed(() => store.state.read.messages);
    const message = ref({});
    const setMessage = item => {
      message.value = item;
    };
    const apiPath = computed(() => `/api/board/content/${String(props.id)}/`);

    return {
      messages, message, apiPath, 
      setMessage
    };
  },
};
</script>