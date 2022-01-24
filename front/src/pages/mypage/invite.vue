<template>
  <AbstractSetting>
    <h3>ユーザー招待</h3>
    <p>
      Googleアカウントで新規招待を行うには下のフォームを入力し送信して下さい。<br />
      LiveLogの場合は招待不要です。詳しくは
      <a href="">ヘルプ</a>をご覧ください。
    </p>

    <Form
      @submit="submit"
      :validation-schema="schema"
      v-slot="{ errors }"
      class="pure-form pure-form-stacked"
    >
      <div class="pure-control-group">
        <label
          >Gmailアドレス（Googleアカウント）:
          <Field name="email" class="pure-input-1" />
        </label>
        <ValidationErrorMessages
          v-if="errors.email"
          :messages="[errors.email]"
        />
      </div>

      <div class="pure-control-group">
        <label
          >入部年度:
          <Field name="year" class="pure-input-1" />
        </label>
        <ValidationErrorMessages v-if="errors.year" :messages="[errors.year]" />
      </div>

      <div class="pure-control-group">
        <label
          >名字:
          <Field name="lastName" class="pure-input-1" />
        </label>
        <ValidationErrorMessages
          v-if="errors.lastName"
          :messages="[errors.lastName]"
        />
      </div>

      <div class="pure-control-group">
        <label
          >名前:
          <Field name="firstName" class="pure-input-1" />
        </label>
        <ValidationErrorMessages
          v-if="errors.firstName"
          :messages="[errors.firstName]"
        />
      </div>

      <div class="pure-control-group">
        <label
          >ふりがな:
          <Field name="furigana" class="pure-input-1" />
        </label>
        <ValidationErrorMessages
          v-if="errors.furigana"
          :messages="[errors.furigana]"
        />
      </div>

      <div class="custom-two-buttons-wrapper">
        <router-link :to="{ name: 'mypage:index' }" class="pure-button return"
          >戻る</router-link
        >
        <button class="pure-button button-primary">
          招待し、招待メールを送信
        </button>
      </div>
    </Form>
  </AbstractSetting>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { Field, Form } from "vee-validate";
import yup from "@/utils/yup.js";
import AbstractSetting from "@/components/AbstractSetting.vue";
import ValidationErrorMessages from "@/components/ValidationErrorMessages.vue";
import { useRouter } from "vue-router";
export default {
  components: {
    Field,
    Form,
    AbstractSetting,
    ValidationErrorMessages,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const canRegisterUser = computed(
      () => store.state.mypage.userInfo.canRegisterUser
    );
    if (!canRegisterUser.value) {
      store.commit("message/addMessage", {
        level: "warning",
        message: "ユーザー登録のための権限が無いようです",
        appname: "mypage/register",
      });
      store.commit("message/addMessage", {
        level: "info",
        message: "このページのリンクからもう一度お試しください",
        appname: "mypage/register",
      });
      router.push({ name: "mypage:index" });
    }

    const submit = (values) => {
      const form = new FormData();
      form.append("last_name", values.lastName);
      form.append("first_name", values.firstName);
      form.append("furigana", values.furigana);
      form.append("email", values.email);
      form.append("year", Number(values.year));
      store.dispatch("mypage/post", {
        path: "/api/mypage/invite/",
        formData: form,
      });
    };

    const schema = yup.object({
      email: yup.string().required().email(),
      year: yup.number().integer().required().min(2000).max(2100),
      lastName: yup.string().required().max(255),
      firstName: yup.string().required().max(255),
      furigana: yup
        .string()
        .required()
        .max(255)
        .matches(/^[ぁ-んー]+$/, "全角ひらがなのみで入力してください"),
    });

    return {
      schema,
      submit,
    };
  },
};
</script>