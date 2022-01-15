<template>
  <form class="pure-form pure-g" @submit="submit">
    <label
      >回生メーリス:
      <input
        type="checkbox"
        name="is_kaisei"
        v-model="params.is_kaisei"
        @change="resetPage"
      />
    </label>
    <label
      >全回メーリス:
      <input
        type="checkbox"
        name="is_zenkai"
        v-model="params.is_zenkai"
        @change="resetPage"
      />
    </label>
    <label
      >ブックマーク:
      <input
        type="checkbox"
        name="is_bookmark"
        v-model="params.is_bookmark"
        @change="resetPage"
      />
    </label>
    <label
      >送信したメーリス:
      <input
        type="checkbox"
        name="is_sender"
        v-model="params.is_sender"
        @change="resetPage"
      />
    </label>
    <input
      type="text"
      name="text"
      placeholder="件名・本文で検索"
      class="formtext"
      id="id_text"
      v-model="params.text"
    />

    <button class="pure-button search" type="submit">検索</button>
  </form>
</template>

<script>
import { onMounted, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
export default {
  name: "searchform",
  setup() {
    const router = useRouter();
    const route = useRoute();
    const params = reactive({
      is_kaisei: false,
      is_zenkai: false,
      is_bookmark: false,
      is_sender: false,
      text: "",
      page: 1,
    });

    const submit = (e) => {
      e.preventDefault();

      // clean params
      const query = {};
      if (params.is_kaisei) {
        query.is_kaisei = true;
      }
      if (params.is_zenkai) {
        query.is_zenkai = true;
      }
      if (params.is_bookmark) {
        query.is_bookmark = true;
      }
      if (params.is_sender) {
        query.is_sender = true;
      }
      if (params.text.length > 0) {
        query.text = params.text;
      }
      if (params.page > 1) {
        query.page = params.page;
      }
      router.push({ query });
      // change only query
    };

    onMounted(() => {
      if (route.query.is_kaisei && route.query.is_kaisei === "true") {
        params.is_kaisei = true;
      }
      if (route.query.is_zenkai && route.query.is_zenkai === "true") {
        params.is_zenkai = true;
      }
      if (route.query.is_bookmark && route.query.is_bookmark === "true") {
        params.is_bookmark = true;
      }
      if (route.query.is_sender && route.query.is_sender === "true") {
        params.is_sender = true;
      }
      if (route.query.text) {
        params.text = route.query.text;
      }
      if (route.query.page && Number(route.query.page) > 1) {
        params.page = Number(route.query.page);
      }
    });

    const resetPage = () => {
      params.page = 1;
    };
    return {
      params,
      submit,
      resetPage,
    };
  },
};
</script>


<style lang="scss" scoped>
form {
  margin-bottom: 1em;
}

.formtext {
  display: inline-block;
  box-sizing: border-box;
  height: 2rem;
  width: calc(100% - 4rem);
  min-width: 10rem;
  max-width: 33rem;
  padding: 0.125rem 0.25rem;
  margin-right: 0.5rem;
  margin-top: 0.5rem;
}
.search {
  display: inline-block;
  box-sizing: border-box;
  height: 2rem;
  width: 3.5rem;
  padding: 0.125rem 0.5rem;
  margin-top: 0.5rem;
}

label {
  display: inline-flex;
  font-size: 0.75rem;
  margin-right: 1rem !important;
  align-items: end;

  input[type="checkbox"] {
    display: inline-block;
    margin-left: 0.2rem;
  }
}
</style>