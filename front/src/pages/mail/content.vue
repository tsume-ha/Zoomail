<template>
  <abstract-content
    :id="id"
    :dataList="messages"
    :oneContentAPIPath="apiPath"
    @setContent="setMessage"
  >
    <template #header>
      <abstract-content-header :path="{name: 'mail:index'}" :text="message.title" hidden/>
    </template>

    <article>
      <header>
        <h4>{{message.title}}</h4>
        <div>
          <time>{{message.created_at}}</time>
          <span>{{message.writer}}</span>
          <button @click="bookmark">
            <img src="@/assets/img/star_yl.png" width="16" height="16" v-if="message.is_bookmarked" alt="bookmarked"/>
            <img src="@/assets/img/star_bk.png" width="16" height="16" v-else alt="not bookmarkd yet"/>
          </button>
        </div>
      </header>
      <div class="message-content card" v-html="message.html"></div>
    </article>
  
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

<style lang="scss" scoped>
article {
  padding: 1.5rem 0;
  header {
    height: auto;
    > div {
      display: flex;
      align-items: center;
      margin: .75rem 0;
      
      > * {
        display: inline-block;
      }
      time {
        font-size: .75em;
        margin-right: .5em;
        flex-grow: 0.1;
        flex-shrink: 0;
        flex-basis: auto;
      }
      span {
        flex-grow: 1;
        flex-shrink: 1;
        flex-basis: auto;
      }
      button {
        background-color: transparent;
        border: none;
        width: 16px;
        height: 16px;
        margin-right: .5em;
        flex-grow: 0;
        flex-shrink: 0;
        flex-basis: 16px;
      }
    }
  }
  div.message-content {
    margin: 1.5rem 0;
    padding: .5rem;
  }
}
</style>

<style lang="scss">
div.message-content p {
  margin: 1rem 0;
  &:first-child {
    margin-top: 0;
  }
  &:last-child {
    margin-bottom: 0;
  }
  a {
    font-style: italic;
  }
}
</style>