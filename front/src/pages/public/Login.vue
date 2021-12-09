<template>
  <article>
    <h3>LOG IN</h3>
    <div class="login-wraper">
      <LoginWithLiveLog />
      <LoginWithGoogle />
    </div>

    <p class="small">
      Googleアカウントでログインするには事前の登録が必要です。<br>
      詳しくはHP係までご連絡ください。
    </p>

    <p id="login-help" class="small">
      <a href="/howto/" target="_blank">ヘルプ：使い方へ</a>
    </p>
  </article>
</template>

<script>
import LoginWithLiveLog from "@/components/LoginWithLiveLog.vue";
import LoginWithGoogle from "@/components/LoginWithGoogle.vue";
import { onMounted } from "vue";
import { useStore } from "vuex";

export default {
  components: {
    LoginWithLiveLog,
    LoginWithGoogle
  },
  setup() {
    const store = useStore();
    onMounted(() => store.commit("message/storeMessageFromCokie"));
  },
};
</script>

<style lang="scss" scoped>
article{
  color: $text-white;
  text-align: center;
  position: relative;

  h3 {
    margin: 1rem;
  }
  .login-wraper {
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  #login-help {
    display: inline-block;
    position: absolute;
    right: 0;
    bottom: 1rem;
    text-align: center;

    a {
      text-decoration: underline;
    }
  }
}
</style>