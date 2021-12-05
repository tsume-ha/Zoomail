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
  </article>
</template>

<script>
import LoginWithLiveLog from "@/components/LoginWithLiveLog.vue";
import LoginWithGoogle from "@/components/LoginWithGoogle.vue";

export default {
  components: {
    LoginWithLiveLog,
    LoginWithGoogle
  },
  setup() {
    
  },
};
</script>

<style lang="scss" scoped>
article{
  color: $text-white;
  text-align: center;

  h3 {
    margin: 1rem;
  }
  .login-wraper {
    display: flex;
    flex-flow: row wrap;
    justify-content: center;
    align-items: center;
  }
}
</style>