<template>
  <article>
    <h3>{{ h3Text }}</h3>
    <div class="card" v-if="status === 'sending'">
      <div class="icon">
        <RotateSquare2 />
      </div>
      <p>
        送信中です。しばらくお待ちください。<br />
        送信完了まで、10秒ほどかかる場合があります。
      </p>
    </div>
    <div class="card" v-else-if="status === 'done'">
      <div class="icon text-success">
        <Icon :icon="['far', 'check-circle']" />
      </div>
      <p>
        通信が完了しました！<br />
        メーリスを{{ totalSendNum }}人に送信しました。
      </p>
      <div class="links right">
        <router-link
          :to="{ name: 'mail:index' }"
          class="pure-button button-primary"
        >
          メーリス一覧へ
        </router-link>
      </div>
    </div>
    <div class="card" v-else-if="status === 'error'">
      <div class="icon text-error">
        <Icon :icon="['fas', 'exclamation-circle']" />
      </div>
      <p>
        エラーが発生し、送信できませんでした。<br />
        送信内容を確認するか、開発者までご連絡ください。
      </p>
      <div class="links left">
        <router-link :to="{ name: 'mail:send' }" class="pure-button return">
          送信画面へ戻る
        </router-link>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { RotateSquare2 } from "vue-loading-spinner";

const store = useStore();
const router = useRouter();
const status = ref("sending");
const totalSendNum = ref(null);

// フォームが無効の時は戻る
if (!store.getters["send/isValidAndDirty"]) {
  router.push({ name: "mail:send" });
} else {
  // APIと通信
  store
    .dispatch("send/send")
    .then((res) => {
      // 正常にPOSTできた時。メーリスのトップページに遷移する
      console.log(res);
      totalSendNum.value = res.data.total_send_num;
      status.value = "done";
      store.commit("send/reset");
    })
    .catch((err) => {
      // 送信エラーが起こった時。遷移しない。
      console.log(err);
      status.value = "error";
    });
}
const h3Text = computed(() => {
  const statusText = {
    sending: "送信中",
    done: "完了",
    error: "エラー",
  };
  return `メーリス送信 - ${statusText[status.value]}`;
});
</script>

<style lang="scss" scoped>
.card {
  text-align: center;
  margin: 2rem auto;
  padding: 1rem 2rem;

  .icon {
    width: 100%;
    height: 5rem;
    padding: 2rem 0;

    > * {
      width: 40px;
      height: 40px;
      display: block;
      margin: 0 auto;
    }
  }
  .links {
    width: 100%;
    margin: 4rem 0 0;
    &.right {
      text-align: right;
    }
    &.left {
      text-align: left;
    }
  }
}
.text-success {
  color: $text-green;
}
.text-error {
  color: $text-red;
}
</style>