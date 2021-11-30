<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/photo">Photo</router-link> | 
    <router-link to="/sound">Sound</router-link> | 
    <router-link to="/kansou">Kansou</router-link> | 
    <router-link to="/mypage">Mypage</router-link> | 
    <router-link to="/mail">Read - index</router-link> | 
    <router-link to="/mail/send">Send</router-link>
  </div>
  <main class="container">
    <router-view />
  </main>
  <message />
</template>

<script>
import { onMounted } from '@vue/runtime-core';
import { useStore } from 'vuex';
import message from './components/message';
export default {
  components: {
    message
  },
  setup() {
    const store = useStore();
    onMounted(store.dispatch("mypage/getUserInfo"));
  }
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
