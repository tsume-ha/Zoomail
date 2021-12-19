<template>
  <article>
    <h3>メーリス送信・入力</h3>
    <form>
      <div class="pure-form pure-form-stacked">
        <send-input-title />
      </div>
      <send-input-to />
      <div class="pure-form pure-form-stacked">
        <send-input-from />
        <send-input-content />
        <send-input-attachments />
        <button
          @click="onClick"
          class="pure-button-primary pure-button"
          :disabled="!isValid"
        >
          確認画面へ
        </button>
      </div>
    </form>
  </article>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import sendInputTitle from "./components/send-input-title.vue";
import sendInputContent from "./components/send-input-content.vue";
import sendInputTo from "./components/send-input-to.vue";
// vue-selectをVue3対応の @beta で利用
import sendInputFrom from "./components/send-input-from.vue";
import sendInputAttachments from "./components/send-input-attachments.vue";
export default {
  components: {
    sendInputTitle,
    sendInputContent,
    sendInputTo,
    sendInputFrom,
    sendInputAttachments,
  },
  setup() {
    const store = useStore();
    const isValid = computed(() => store.getters["send/isValidAndDirty"]);

    const router = useRouter();
    const onClick = (e) => {
      e.preventDefault();
      // 確認画面に行く前にValidationを走らせる
      store.commit("send/validateAll");

      if (isValid.value) {
        // validの時は確認画面へ
        router.push("/mail/send/confirm");
      } else {
        // invalidの時はメッセージを出して遷移させない
        store.commit("message/addMessage", {
          level: "warning",
          message: "不正なフィールドがあります。",
          appname: "mail/send",
        });
      }
    };
    return {
      isValid,
      onClick,
    };
  },
};
</script>
<style lang="scss" scoped>
.form-one-row {
  margin: 1rem 0;
}
</style>