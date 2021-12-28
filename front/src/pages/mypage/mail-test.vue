<template>
  <abstract-setting :loading="loading">
    <h3>メーリス受信テスト</h3>
      <form class="pure-form pure-form-stacked">
        <div class="pure-control-group">
          <label for="stacked-email">現在設定されているメールアドレス</label>
          <input type="email" id="stacked-email"
            :value="showEmailAddress ? receiveEmail : '***************'"
            readonly
            class="pure-input-1"
          />
        </div>

        <div class="pure-controls">
          <button
            @click.prevent="showEmailAddress=!showEmailAddress"
            class="pure-button"
            v-text="showEmailAddress ? 'メールアドレスを隠す' : 'メールアドレスを表示する'"
            ></button>
        </div>

        <div class="pure-control-group">
        <p class="small">
          メーリスがきちんと受信できるか確かめるために、テストメールを送信します。<br>
          テストメールの送信は5分に1回行うことができます。
        </p>
        </div>

        <div class="pure-control-group custom-two-buttons-wrapper">
          <router-link to="../"  class="pure-button">戻る</router-link>
          <button @click.prevent="send" class="pure-button button-primary">
            送信する
          </button>
        </div>

      </form>
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
    const loading = computed(() => store.state.mypage.loading);

    const send = () => {
      const formData = new FormData();
      formData.append("send", true);
      store.dispatch("mypage/post", {path: "/api/mypage/mail-test/", formData});
    };

    return {
      receiveEmail, showEmailAddress, loading,
      send
    };
  },
};
</script>