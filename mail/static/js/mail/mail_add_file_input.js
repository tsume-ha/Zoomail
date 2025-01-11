document.addEventListener('DOMContentLoaded', function () {
    const fileInputContainer = document.getElementById('file-input-container');
    const addFileButton = document.getElementById('add-file-button');
    let totalForms = document.getElementById("id_attachments-TOTAL_FORMS");
    let maxForms = document.getElementById("id_attachments-MAX_NUM_FORMS");
    let formCount = parseInt(totalForms.value, 10);

    function addFileInput() {
        const newFormIndex = formCount;
        if (formCount >= parseInt(maxForms.value, 10)) {
            // フォーム数の上限に達した場合は何もしない
            return;
        }
        const emptyFormTemplate = `
        <div class="mb-2">
          <input type="file" name="attachments-${newFormIndex}-file" class="form-control" id="id_attachments-${newFormIndex}-file">
        </div>
      `;
        // 新しいフォームを追加
        fileInputContainer.insertAdjacentHTML('beforeend', emptyFormTemplate);
        // 総フォーム数を更新
        formCount++;
        totalForms.value = formCount;
    }

    addFileButton.addEventListener('click', addFileInput);
});