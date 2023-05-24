<template>
  <Header :status="'menuClosed'" />
  <main class="container">
    
    <article>
      <h2>Zoomailへようこそ！</h2>
      <p>
        <em>Zoomail</em>は、京大アンプラグドの<em>メール配信プラットフォーム</em>です。<br>
        このZoomailを通して、皆さんにはサークルの全体連絡である<em>メーリス</em>が届きます。<br>
        日常的な連絡はSlackで行われますが、Zoomailからは<em>ライブの告知</em>や<em>合宿のお知らせ</em>、<em>会費の振り込み</em>など、<em>サークル運営にかかわる重要な連絡</em>が送られてきます！
      </p>
      <p>このフォームにメールアドレスを登録して、メーリスを受信しましょう</p>

      <form @submit="submit" class="pure-form pure-form-stacked">
        <div class="pure-control-group">
          <label for="id_email">メールアドレス:</label>
          <input
            type="email"
            name="email"
            v-model="formData.email"
            maxlength="255"
            required=""
            id="id_email"
            class="pure-input-1"
          />
          <p class="small">このメールアドレスにメーリスが届きます。<br>LiveLogに登録したものと異なるメールアドレスでも受信可能です。</p>
          <ValidationErrorMessages v-if="errorMessages?.email?.length" :messages="errorMessages.email.map(d => d.message)" />
        </div>
        
        <div class="pure-control-group">
          <label for="id_last_name">苗字:</label>
          <input
            type="text"
            name="last_name"
            v-model="formData.lastName"
            maxlength="255"
            required=""
            placeholder="京大"
            id="id_last_name"
            class="pure-input-1"
          />
          <ValidationErrorMessages v-if="errorMessages?.lastName?.length" :messages="errorMessages.lastName.map(d => d.message)" />
        </div>

        <div class="pure-control-group">
          <label for="id_first_name">名前:</label>
          <input
            type="text"
            name="first_name"
            v-model="formData.firstName"
            maxlength="255"
            required=""
            placeholder="太郎"
            id="id_first_name"
            class="pure-input-1"
          />
          <ValidationErrorMessages v-if="errorMessages?.firstName?.length" :messages="errorMessages.firstName.map(d => d.message)" />
        </div>

        <div class="pure-control-group">
          <label for="id_furigana">ふりがな:</label>
          <input
            type="text"
            name="furigana"
            v-model="formData.furigana"
            maxlength="255"
            required=""
            placeholder="きょうだいたろう"
            id="id_furigana"
            class="pure-input-1"
          />
          <p class="small">ひらがなのみ（五十音順のソートに使われます）</p>
          <ValidationErrorMessages v-if="errorMessages?.furigana?.length" :messages="errorMessages.furigana.map(d => d.message)" />
        </div>

        <div class="pure-control-group">
          <label for="id_nickname">ニックネーム:</label>
          <input
            type="text"
            name="nickname"
            v-model="formData.nickname"
            maxlength="255"
            placeholder="たろー"
            id="id_nickname"
            class="pure-input-1"
          />
          <p class="small">メーリスを送信するときの表示名になります</p>
          <ValidationErrorMessages v-if="errorMessages?.nickname?.length" :messages="errorMessages.nickname.map(d => d.message)" />
        </div>

        <div class="pure-controls">
          <button type="submit" class="pure-button button-primary">登録する！</button>
        </div>
      </form>
    </article>

  </main>
  <Footer />
  
  <Loading 
      v-model:active="isLoading"
      :can-cancel="false"
      :is-full-page="true"
      color="#386471"
      />
</template>

<script setup>
import { reactive, ref } from "vue";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/css/index.css";
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import ValidationErrorMessages from "@/components/ValidationErrorMessages.vue";
import axios from "./utils/axios";

const isLoading = ref(true);

const formData = reactive({
  email: "",
  lastName: "",
  firstName: "",
  furigana: "",
  nickname: "",
});

const errorMessages = ref({});

(() => {
  axios.get("/api/tempuser/").then(res => {
    formData.email = res?.data?.email ? res.data.email : "";
    formData.lastName = res?.data?.lastName ? res.data.lastName : "";
    formData.firstName = res?.data?.firstName ? res.data.firstName : "";
    formData.furigana = res?.data?.furigana ? res.data.furigana : "";
    formData.nickname = res?.data?.nickname ? res.data.nickname : "";
  }).finally(() => {
    isLoading.value = false;
  });
})();

const submit = (e) => {
  e.preventDefault();
  isLoading.value = true;
  const cleanFormData = new FormData();
  cleanFormData.append("email", formData.email);
  cleanFormData.append("last_name", formData.lastName);
  cleanFormData.append("first_name", formData.firstName);
  cleanFormData.append("furigana", formData.furigana);
  cleanFormData.append("nickname", formData.nickname);
  axios.post("/api/first-register/", cleanFormData).then(() => {
    isLoading.value = false;
    location.replace("/");
  }).catch(error => {
    console.error(error);
    if (error.response.status === 400) {
      errorMessages.value = {...error.response.data};
    }
  }).finally(() => {
    isLoading.value = false;
  });
};


</script>
<style lang="scss" scoped>
main {
  position: relative;
  background-color: $bg-light;
  > article {
    color: $text-black;
    > p {
      margin: 1rem 0;
      > em {
        font-weight: 800;
        font-style: normal;
      }
    }
  }
}
button[type="submit"] {
  margin-top: 2rem;
}
</style>
