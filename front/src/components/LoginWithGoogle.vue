<template>
  <a href="/auth/login/google-oauth2" id="G-login" alt="Sign in with Google">
    Sign in with Google
  </a>
</template>

<style lang="scss" scoped>
a#G-login{
  display: inline-block;
  color: transparent;
  text-decoration: none;
  background-image: url("../assets/img/btn_google_signin_light_normal_web@2x.png");
  background-size: 192px 46px;
  background-color: transparent;
  box-sizing: content-box;
  height: 46px;
  width: 192px;
  margin: 1rem;
  flex-shrink: 0;
  font-size: 0;
  border: transparent 2px solid;
}
a#G-login:hover{
  text-decoration: none;
  background-image: url("../assets/img/btn_google_signin_light_focus_web@2x.png");
  border: $text-white 2px solid;
}
</style>