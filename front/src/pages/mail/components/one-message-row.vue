<template>
  <section class="card" :id="'message-id-'+String(message.id)">
    <h4>
      <router-link :to="link">{{message.title}}</router-link>
      <Icon icon="paperclip" v-if="message.attachments.length" />
    </h4>
    <div>
      <time>{{message.created_at}}</time>
      <span>{{message.writer}}</span>
      <button @click="bookmark">
        <img src="@/assets/img/star_yl.png" width="16" height="16" v-if="message.is_bookmarked" alt="bookmarked"/>
        <img src="@/assets/img/star_bk.png" width="16" height="16" v-else alt="not bookmarkd yet"/>
      </button>
    </div>
    <p>
      {{trimed}}
    </p>
  </section>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
export default {
  props: {
    message: {required: true, type: Object}
  },
  setup(props) {
    const store = useStore();

    const message = computed(() => props.message);
    const trimed = computed(() => {
      const text = message.value.content;
      let count = text.indexOf("\n");
      if (count < 0) {
        count = 0;
      }
      return text.slice(count, count+200);
    });
    const link = computed(() => `/mail/${String(message.value.id)}`);

    const bookmark = () => {
      store.dispatch("read/toggleBookmark", message.value.id);
    };
    return {
      bookmark,
      trimed, link
    };
  }
};
</script>

<style lang="scss" scoped>
section {
  display: block;
  margin: .4em 0;
  padding: .5em;
  color: $text-black;
  
  > * {
    margin: .5em;
  }
  > div {
    display: flex;
    align-items: center;
    
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
  > h4 {
    display: block;
    font-size: 1.25em;
    // color: $text-link-blue;
    text-decoration: underline;
  }

  > p {
    display: block;
    line-height: 1.25;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }
}

</style>