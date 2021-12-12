<template>
  <form class="pure-form pure-g" @submit="submit">
      <input type="checkbox" name="is_kaisei" id="is_kaisei" v-model="params.is_kaisei">
      <label for="is_kaisei">回生メーリスのみ:</label>
      
      <input type="checkbox" name="is_zenkai" id="is_zenkai" v-model="params.is_zenkai">
      <label for="is_zenkai">全回メーリスのみ:</label>
      
      <input type="checkbox" name="is_bookmark" id="is_bookmark" v-model="params.is_bookmark">
      <label for="is_bookmark">ブックマークのみ:</label>
      
      <input type="checkbox" name="is_sender" id="is_sender" v-model="params.is_sender">
      <label for="is_sender">送信したメーリスのみ:</label>

    <input type="text" name="text" placeholder="件名・本文で検索" class="formtext" id="id_text" v-model="params.text">
    
    <button class="pure-button search">検索</button>
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

    const submit = e => {
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

    return {
      params,
      submit
    };
  }
};
</script>


<style scoped>
form {
  margin-bottom: 1em;
}

.formtext{
  display: inline-block;
  box-sizing: border-box;
  width: calc(100% - 4em);
  min-width: 10em;
  max-width: 30em;
  padding: 0.125em .25em;
  margin: 0 0.5em 0 0;
}
.search{
  display: inline-block;
  box-sizing: border-box;
  width: 3.5em;
  padding: 0.125em 0.5em;
}

input[type="checkbox"] {
  display: none;
}

label{
    display: inline-block;
    position: relative;
    height: 1rem;
    padding: 0.5rem 3rem 1rem 0;
    margin: 0 0 0.5rem;
    font-size: 0.7rem;
    line-height: 0.7rem;
}
label:before{
  display: inline-block;
  content: "";
  position: absolute;
    right: 0.4rem;
    top: 0.3rem;
  width: 2.4rem;
  height: 1.2rem;
  margin: 0;
  padding: 0;
  border: 1px solid #eee;
  border-radius: 1rem;
  transition: 0.2s;
}
label:after{
  display: block;
  content: "";
  position: absolute;
  top: 0.44rem;
  right: 1.7rem;
  width: 0.9rem;
  height: 0.9rem;
  border-radius: 0.75rem;
  background-color: #eee;
  transition: 0.2s;
}
input:checked + label:before{
  border-color: #0ee08a;
}
input:checked + label:after{
  right: 0.62rem;
  background-color: #0ee08a;
}

</style>