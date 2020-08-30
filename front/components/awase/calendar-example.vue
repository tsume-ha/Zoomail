<template>
  <div>
    <p class="small">
      色分けは、その時間帯に参加できない人の人数を表しています。<br>
      回答していない人は数に含まれていません。
    </p>
    <p>
      凡例：参加できない人数...0人（回答者は全員参加できる）<span class="NG0"></span><br>
      1人<span class="NG1"></span><br>
      2人<span class="NG2"></span><br>
      3人以上<span class="NG3"></span><br>
      全員未回答もしくは集計範囲外<span></span><br>
    </p>
  </div>
</template>
<script>
export default {
  
}
</script>
<style scoped>
@import "./calendar-color.css";
#exapmle span{
  display: inline-block;
  position: relative;
  width: 1rem;
  height: 1rem;
  padding: 0;
  margin: 0 0 0 0.5rem;
  border: 1px solid #aaa;
}
</style>