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


class FileEditForm(forms.ModelForm):
    filename = forms.CharField(label="ファイル名", max_length=255)
    delete = forms.BooleanField(required=False, label="削除")

    class Meta:
        model = File
        fields = ["file", "filename"]

    @property
    def file_input(self):
        return self.fields["file"].widget.render(
            name=self.add_prefix("file"), value="", attrs={"class": "form-control"}
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].label = "ファイル"
        self.fields["file"].widget = forms.FileInput(attrs={"class": "form-control"})
        self.fields["filename"].widget.attrs.update({"class": "form-control"})
        self.fields["delete"].widget.attrs.update({"class": "form-check-input"})
        self.file_ext = ""
        if self.instance and getattr(self.instance, "pk", None):
            full_name = self.instance.filename
            basename, dot, ext = full_name.rpartition(".")
            if dot:
                self.initial["filename"] = basename
                self.file_ext = "." + ext
            else:
                self.file_ext = ""

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("delete"):
            instance.is_deleted = True
        if "file" in self.changed_data:
            uploaded_file = self.files.get("file")
            if uploaded_file:
                instance.filename = uploaded_file.name
        else:
            input_basename = self.cleaned_data.get("filename", "")
            instance.filename = input_basename + self.file_ext
        if commit:
            instance.save()
        return instance
