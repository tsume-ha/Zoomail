<template>
  <article>
    <h3>icalフィード</h3>
    <div class="card">
      <p>Googleカレンダーで例会教室の情報を表示させることができます。<br /></p>
      <p>設定方法は書いてる途中です...</p>
      <form class="pure-form">
        <label
          >登録用URL
          <input
            type="url"
            readonly
            value="https://message.ku-unplugged.net/meeting_room/meeting_room.ics"
        /></label>
      </form>
      <p>このURLをパソコン版Googleカレンダーから登録します。</p>
    </div>
  </article>
</template>

<style lang="scss" scoped>
.card {
  padding: 1rem 0.5rem;
}
input[type="url"] {
  width: 100%;
}
</style>