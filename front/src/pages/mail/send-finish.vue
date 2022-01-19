<template>
  <article>
    <h3>{{ h3Text }}</h3>
    <div class="card">
      <p>
        <template v-for="text in textMessage" :key="text">
          {{ text }}<br />
        </template>
      </p>
    </div>
  </article>
</template>

<script setup>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

// フォームが無効の時は戻る
if (!store.getters["send/isValidAndDirty"]) {
  router.push({ name: "mail:send" });
}

// APIと通信
const sending = ref(true);
const textMessage = ref([
  "送信中です。しばらくお待ちください。",
  "送信完了まで、10秒ほどかかる場合があります。",
]);
store
  .dispatch("send/send")
  .then((res) => {
    // 正常にPOSTできた時。メーリスのトップページに遷移する
    console.log(res);
    textMessage.value = [
      "通信が完了しました！",
      "5秒後にメーリス一覧のページに遷移します。",
    ];
    // setTimeout(() => {
    //   router.push({ name: "mail:index" });
    // }, 5000);
  })
  .catch((err) => {
    // 送信エラーが起こった時。遷移しない。
    console.log(err);
  })
  .finally(() => {
    sending.value = false;
  });
const h3Text = computed(() =>
  sending.value ? "メーリス送信 - 送信中" : "メーリス送信 - 完了"
);
</script>

<style lang="scss" scoped>
.card {
  text-align: center;
  margin: 2rem auto;
  padding: 3rem 2rem;
}
</style>