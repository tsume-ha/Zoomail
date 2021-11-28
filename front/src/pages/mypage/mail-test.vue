<template>
  <abstract-setting :loading="loading">
    <section>
      <div class="mt-4 mb-2">
        <span class="mb-2">現在設定されているメールアドレス</span>
        <br>
        <span v-if="showEmailAddress">
          {{receiveEmail}}
        </span>
        <span v-else>
          ******************
        </span>
      </div>
      
      <div class="mb-3">
        <button
          v-if="showEmailAddress"
          @click="showEmailAddress=false"
          class="btn btn-sm btn-light"
          >メールアドレスを隠す</button>
        <button
          v-else
          @click="showEmailAddress=true"
          class="btn btn-sm btn-light"
          >メールアドレスを表示する</button>
      </div>

      <p class="small">
        メーリスがきちんと受信できるか確かめるために、テストメールを送信します。<br>
        テストメールの送信は5分に1回行うことができます。
      </p>

      <router-link to="../"  class="btn btn-secondary mx-2 my-3">戻る</router-link>
      <button @click.prevent="send" class="btn btn-info mx-2 my-3">
        送信する
      </button>

    </section>
  </abstract-setting>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import AbstractSetting from "../../components/AbstractSetting.vue";
export default {
  components: {
    AbstractSetting
  },
  setup() {
    const store = useStore();
    const showEmailAddress = ref(false);
    const receiveEmail = computed(() => store.state.mypage.userInfo.receiveEmail);
    const loading = computed(() => store.state.mypage.loading)

    const send = () => {
      const formData = new FormData();
      formData.append("send", true)
      store.dispatch("mypage/post", {path: "/api/mypage/mail-test/", formData});
    };

    return {
      receiveEmail, showEmailAddress, loading,
      send
    }
  },
}
</script>