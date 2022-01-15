<template>
  <a href="/auth/login/auth0" class="livelogin">
    <span>Log in with</span><img src="../assets/img/livelog.png" width="80" height="59" alt="LiveLog" />
  </a>
</template>

<style lang="scss" scoped>
a.livelogin{
  display: inline-flex;
  position: relative;
  justify-content: center;
  align-items: center;
  box-sizing: content-box;
  width: 192px;
  height: 64px;
  border-radius: 4px;
  color: #666!important;
  margin: 0 0.5rem;
  padding: 0 6px;
  border: transparent 2px solid;
  text-decoration: none;
  flex-shrink: 0;
  background-color: #fcf8e3;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}
a.livelogin:hover{
  text-decoration: underline;
  border: $text-white 2px solid;
}
a.livelogin span{
  display: inline-block;
  font-size: 16px;
  margin: 0;
  padding: 0;
}
a.livelogin img{
  display: inline-block;
  margin: 0;
  padding: 0;
}
</style>