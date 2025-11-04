document.addEventListener('DOMContentLoaded', function () {
  const fileInputContainer = document.getElementById('file-input-container');
  const addFileButton = document.getElementById('add-file-button');
  let totalForms = document.getElementById('id_attachments-TOTAL_FORMS');  // Djangoのformset管理用
  let formCount = parseInt(totalForms.value, 10);

  // ファイル追加ボタンの処理
  addFileButton.addEventListener('click', function () {
    const newFormIndex = formCount;
    const emptyFormTemplate = `
      <div class="mb-2 file-input-wrapper" data-index="${newFormIndex}">
        <div class="d-flex align-items-center gap-2">
          <input type="file" name="attachments-${newFormIndex}-file" class="form-control" id="id_attachments-${newFormIndex}-file">
          <button type="button" class="btn btn-outline-danger px-3 remove-file-button" data-index="${newFormIndex}">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              class="lucide lucide-x">
              <path d="M18 6 6 18" />
              <path d="m6 6 12 12" />
            </svg>
          </button>
        </div>
      </div>
    `;

    // 新しいフォームを追加
    fileInputContainer.insertAdjacentHTML('beforeend', emptyFormTemplate);
    formCount++;
    totalForms.value = formCount;  // 総フォーム数を更新

    // 削除ボタンのイベントリスナーを再設定
    attachRemoveEvent();
  });

  // 削除ボタンの処理
  function attachRemoveEvent() {
    const removeButtons = document.querySelectorAll('.remove-file-button');
    removeButtons.forEach(function (button) {
      button.addEventListener('click', function (event) {
        const fileInputWrapper = event.target.closest('.file-input-wrapper');
        if (fileInputWrapper) {
          fileInputWrapper.remove();  // フォーム要素を削除
          formCount--;
          totalForms.value = formCount;  // 総フォーム数を減らす
          renumberForms();  // 残りのフォームのインデックスを再番号付け
        }
      });
    });
  }

  // 削除後の再番号付け処理
  function renumberForms() {
    const fileWrappers = fileInputContainer.querySelectorAll('.file-input-wrapper');
    fileWrappers.forEach((wrapper, index) => {
      const inputFile = wrapper.querySelector('input[type="file"]');
      const removeButton = wrapper.querySelector('.remove-file-button');
      const newIndex = index;

      inputFile.name = `attachments-${newIndex}-file`;
      inputFile.id = `id_attachments-${newIndex}-file`;
      wrapper.setAttribute('data-index', newIndex);
      removeButton.setAttribute('data-index', newIndex);
    });
  }

  // 初期削除ボタンのイベントを設定
  attachRemoveEvent();
});
