from django import forms
from .models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            "file",
        ]

    def save(self, commit=True):
        # インスタンス生成（commit=Falseにより保存前の状態）
        instance = super().save(commit=False)
        # リクエストから渡されたアップロードファイルを取得
        uploaded_file = self.files.get("file")
        if uploaded_file:
            # ここでアップロード時のオリジナルのファイル名（日本語が含まれる）を取得
            instance.filename = uploaded_file.name
        if commit:
            instance.save()
        return instance
