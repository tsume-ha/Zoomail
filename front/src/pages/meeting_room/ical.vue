<template>
  <article>
    <h3>Googleカレンダー連携</h3>
    <div class="card">
      <p>
        Googleカレンダーで例会教室の情報を表示させることができます。<br />
        <img
          class="pure-img"
          src="@/assets/img/meeting_room/complete.png"
          alt="設定が完了し表示に成功したGoogleカレンダーの画面"
        />
      </p>
      <p>
        設定方法は書いてる途中です...今度わかりやすいように画像を足します...
      </p>
      <p>
        パソコン版Googleカレンダーからのみ設定できます。スマホ版からは設定できません。<br />
        パソコン版で設定したあと、スマホからでも表示できます。
      </p>
      <p>Googleカレンダーにアクセスします</p>
      <p>
        左のメニューから「他のカレンダー」の右にある「+」ボタンを押します。<br />
        出てくるメニューの中から「URLで追加」を押します。
      </p>
      <p>カレンダーのURL欄に、以下のURLを登録します。</p>
      <form class="pure-form">
        <label
          >登録用URL
          <input
            type="url"
            readonly
            value="https://message.ku-unplugged.net/meeting_room/meeting_room.ics"
        /></label>
      </form>
      <p>「カレンダーを一般公開する」のチェックは入れなくていいです。</p>
      <p>
        URLをコピペしたら「カレンダーを追加」ボタンを押します。<br />数秒でカレンダーがインポートされるはずです。
      </p>
      <p>
        名前の変更<br />
        「他のカレンダーの設定」から表示名を変更できます。
      </p>
      <p>スマホ版での表示方法は今度書きます。</p>
    </div>
    <router-link :to="{ name: 'meeting_room:index' }" class="pure-button return"
      >戻る</router-link
    >
  </article>
</template>

<style lang="scss" scoped>
.card {
  padding: 1rem 0.5rem;
  margin-bottom: 2rem;
}
input[type="url"] {
  width: 100%;
}
</style>