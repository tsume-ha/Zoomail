<template>
  <abstract-setting :loading="loading">
    <h3>メーリス受信設定</h3>
    <form @submit="submit" class="pure-form pure-form-stacked">

      <div class="pure-control-group">
        <label for="id_last_name">受信用メールアドレス:</label>
        <input
          type="email"
          name="last_name"
          v-model="formData.receiveEmail"
          maxlength="254"
          class="pure-input-1"
          required="false"
          id="id_last_name"
          >
        <p class="small">
          メーリスを受信するメールアドレスを指定してください。<br>
          空白の場合は、ログインに用いるGmailアドレスか、
          LiveLogアカウントに登録されたメールアドレスになります。
        </p>
      </div>

      <div class="pure-control-group">
        <label for="id_send_mail" class="">メーリスを受信する:</label>
        <input
          type="checkbox"
          name="send_mail"
          v-model="formData.sendMail"
          id="id_send_mail"
        >
        <p class="small">
            メーリスを受け取りたくない場合はチェックを外してください。<br>
            チェックが外されると、全回・回生メーリスともに送信されないようになりますが、<br>
            このサイトにログインし、メーリスを確認することは出来ます。
        </p>
      </div>

      

      <div class="custom-two-buttons-wrapper">
        <router-link :to="{name: 'mypage:index'}" class="pure-button">戻る</router-link>
        <button type="submit" class="pure-button button-primary">
          更新
        </button>
      </div>

    </form>
  </abstract-setting>
</template>

<script>
import { computed, onMounted, reactive } from "vue";
import { useStore } from "vuex";
import AbstractSetting from "../../components/AbstractSetting.vue";
export default {
  components: {
    AbstractSetting
  },
  setup() {
    const store = useStore();
    const formData = reactive({
      receiveEmail: "",
      sendMail: true
    });

    const loading = computed(() => store.state.mypage.loading);


    onMounted(() => {
      // formDataの初期値設定
      const userInfo = store.state.mypage.userInfo;
      formData.receiveEmail = userInfo.receiveEmail;
      formData.sendMail = userInfo.sendMail;
    });

    const submit = e => {
      e.preventDefault();
      const cleanFormData = new FormData();
      cleanFormData.append("receive_email", formData.receiveEmail);
      cleanFormData.append("send_mail", formData.sendMail);
      store.dispatch("mypage/post", {path: "/api/mypage/mail-settings/", formData: cleanFormData});
    };


    return {
      formData, loading,
      submit
    };
  },
};
</script>