<template>
  <div>
    <router-link to="./input/" class="enter text-center text-sm-left">入力する</router-link>
    <span
      @click="isOpened=!isOpened"
      id="menu_sw"
      class="text-center text-sm-left"
      :class="{'active': isOpened}"
      >設定変更</span>
    <div
      id="submenu"
      :class="{'active': isOpened}"
      >
      <a href="./update/" class="text-center text-sm-left">カレンダーの名前、説明文の変更</a>
      <a href="./update/" class="text-center text-sm-left">集計期間（日にち）の変更</a>
      <router-link to="./hours/" class="text-center text-sm-left">集計時間（時間帯）の変更</router-link>
      <a href="./urlkey/" class="text-center text-sm-left">招待URLの確認</a>
      <a href="./user/" class="text-center text-sm-left">カレンダーユーザーの変更</a>
      <a href="./leave/" class="text-center text-sm-left text-danger">この日程調整から退会する</a>
      <a href="./delete/" class="text-center text-sm-left text-danger">カレンダーを削除するページへ</a>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      isOpened: false,
    }
  }
}
</script>

<style scoped>
a, span#menu_sw{
	display: block;
	font-size: 1rem;
	margin: 0;
	padding: 0.4rem 0.5rem;
	color: #0480a9;
	border: none;
	background-color: #c9e9f1;
  cursor: pointer;
}
a.enter{
	color: #218c3a;
	background-color: #caf2d4;
}
a.hover{
	background-color: #e4f4f8;
}
a.enter.hover{
	background-color: #afecbd;
}
span.active.hover,
div#submenu a.hover{
	background-color: #e4f4f8;
}
a#menu_sw{
	margin-bottom: 0;
}
div#submenu{
	max-height: 0;
	overflow-y: hidden;
	transition: 0.3s;
}
@media screen and (min-width: 576px) {
div#submenu{
	border-left: 2px solid #aaa;
}
}

div#submenu.active{
  max-height: 300px;
  overflow-y: overflow;
}
</style>