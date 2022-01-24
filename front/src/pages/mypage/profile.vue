<template>
  <abstract-setting :loading="loading">
    <h3>登録情報変更</h3>
    <form @submit="submit" class="pure-form pure-form-stacked">
      <div class="pure-control-group">
        <label for="id_last_name">名字:</label>
        <input
          type="text"
          name="last_name"
          v-model="formData.lastName"
          maxlength="255"
          required=""
          id="id_last_name"
          class="pure-input-1"
        />
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
          class="pure-input-1"
        />
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
          class="pure-input-1"
        />
      </div>

      <div class="pure-control-group">
        <label for="id_nickname">ニックネーム:</label>
        <input
          type="text"
          name="nickname"
          v-model="formData.nickname"
          maxlength="255"
          id="id_nickname"
          class="pure-input-1"
        />
      </div>

      <div class="pure-controls custom-two-buttons-wrapper">
        <router-link :to="{ name: 'mypage:index' }" class="pure-button return"
          >戻る</router-link
        >
        <button type="submit" class="pure-button button-primary">更新</button>
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
    AbstractSetting,
  },
  setup() {
    const store = useStore();
    const formData = reactive({
      lastName: "",
      firstName: "",
      furigana: "",
      nickname: "",
    });

    const loading = computed(() => store.state.mypage.loading);
    const userInfo = computed(() => store.state.mypage.userInfo);

    const setInitialData = () => {
      formData.lastName = userInfo.value.lastName;
      formData.firstName = userInfo.value.firstName;
      formData.furigana = userInfo.value.furigana;
      formData.nickname = userInfo.value.nickname;
    };

    onMounted(() => setInitialData());
    store.watch(
      (_state, getters) => getters["mypage/hasUserInfo"],
      () => {
        setInitialData();
      }
    );

    const submit = (e) => {
      e.preventDefault();
      const cleanFormData = new FormData();
      cleanFormData.append("last_name", formData.lastName);
      cleanFormData.append("first_name", formData.firstName);
      cleanFormData.append("furigana", formData.furigana);
      cleanFormData.append("nickname", formData.nickname);
      store.dispatch("mypage/post", {
        path: "/api/mypage/profile/",
        formData: cleanFormData,
      });
    };

    return {
      formData,
      loading,
      submit,
    };
  },
};
</script>