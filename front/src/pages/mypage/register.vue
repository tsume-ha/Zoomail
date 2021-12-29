<template>
  <AbstractSetting>
    <h3>ユーザー登録</h3>
    <p>
      Googleアカウントで新規登録を行うには下のフォームを入力し送信して下さい。<br>
      LiveLogの場合は不要です。詳しくは
      <a href="">ヘルプ</a>をご覧ください。
    </p>
    <form @submit.prevent="submit" class="pure-form pure-form-stacked">
    
      <div class="pure-control-group">
        <label for="id_email">Gmailアドレス（Googleアカウント）:</label>
        <input
          type="email"
          name="email"
          v-model="formData.email"
          maxlength="254"
          required=""
          id="id_email"
          class="pure-input-1">
      </div>

      <div class="pure-control-group">
        <label for="id_year">入部年度:</label>
        <input
          type="number"
          name="year"
          v-model="formData.year"
          placeholder="2020"
          required=""
          id="id_year"
          class="pure-input-1">
      </div>

      <div class="pure-control-group">
        <label for="id_last_name">名字:</label>
        <input
          type="text"
          name="last_name"
          v-model="formData.lastName"
          maxlength="255"
          required=""
          id="id_last_name"
          class="pure-input-1">
      </div>

      <div class="pure-control-group">
        <label for="id_first_name">名前:</label>
        <input
          type="text"
          name="first_name"
          v-model="formData.firstName"
          maxlength="255"
          required=""
          id="id_first_name"
          class="pure-input-1">
      </div>

      <div class="pure-control-group">
        <label for="id_furigana">ふりがな:</label>
        <input
          type="text"
          name="furigana"
          v-model="formData.furigana"
          maxlength="255"
          required=""
          id="id_furigana"
          class="pure-input-1">
      </div>

      <div class="custom-two-buttons-wrapper">
        <router-link :to="{name: 'mypage:index'}" class="pure-button">戻る</router-link>
        <button class="pure-button button-primary">登録</button>
      </div>
    </form>
  </AbstractSetting>
</template>

<script>
import { reactive } from "vue";
import { useStore } from "vuex";
import AbstractSetting from "../../components/AbstractSetting.vue";
export default {
  components: {
    AbstractSetting
  },
  setup() {
    const store = useStore();
    const formData = reactive({
      email: "",
      year: null,
      lastName: "",
      firstName: "",
      furigana: "",
    });
    const submit = () => {
      const form = new FormData();
      form.append("last_name", formData.lastName);
      form.append("first_name", formData.firstName);
      form.append("furigana", formData.furigana);
      form.append("email", formData.email);
      form.append("year", formData.year);
      store.dispatch("mypage/post", {path: "/api/mypage/register/", formData: form});
    };

    return {
      formData,
      submit
    };
  }
};
</script>