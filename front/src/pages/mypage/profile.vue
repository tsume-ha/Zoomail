<template>
  <abstract-setting>
    <form @submit="submit">
      <ul>
        <li class="form-group row">
          <label for="id_last_name">名字:</label>
          <input
            type="text"
            name="last_name"
            v-model="formData.lastName"
            maxlength="255"
            class="form-control"
            required=""
            id="id_last_name">
        </li>
          
        <li class="form-group row">
          <label for="id_first_name">名前:</label>
          <input
            type="text"
            name="first_name"
            v-model="formData.firstName"
            maxlength="255"
            class="form-control"
            required=""
            id="id_first_name">
        </li>
          
        <li class="form-group row">
          <label for="id_furigana">ふりがな:</label>
          <input
            type="text"
            name="furigana"
            v-model="formData.furigana"
            maxlength="255"
            class="form-control"
            required=""
            id="id_furigana">
        </li>

        <li class="form-group row">
          <label for="id_nickname">ニックネーム:</label>
          <input
            type="text"
            name="nickname"
            v-model="formData.nickname"
            maxlength="255"
            class="form-control"
            id="id_nickname">
        </li>
        <li>
          <button type="submit" class="btn btn-info mx-2 my-3">
            更新
          </button>

        </li>

      </ul>
    </form>
  </abstract-setting>
</template>

<script>
import { onMounted, reactive } from "vue";
import { useStore } from "vuex"
import AbstractSetting from "../../components/AbstractSetting.vue"
export default {
  components: {
    AbstractSetting
  },
  setup() {
    const store = useStore();
    const formData = reactive({
      lastName: "",
      firstName: "",
      furigana: "",
      nickname: ""
    });

    onMounted(() => {
      // formDataの初期値設定
      const userInfo = store.state.mypage.userInfo;
      formData.lastName = userInfo.lastName;
      formData.firstName = userInfo.firstName;
      formData.furigana = userInfo.furigana;
      formData.nickname = userInfo.nickname;
    });

    const submit = e => {
      e.preventDefault();
      const cleanFormData = new FormData();
      cleanFormData.append("last_name", formData.lastName);
      cleanFormData.append("first_name", formData.firstName);
      cleanFormData.append("furigana", formData.furigana);
      cleanFormData.append("nickname", formData.nickname);
      store.dispatch("mypage/post", {path: "/api/mypage/profile/", formData: cleanFormData})
    }
    return {
      formData,
      submit
    }
  },
}
</script>