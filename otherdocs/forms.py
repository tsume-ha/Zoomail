from django import forms

from .models import Content


class UploadForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'file', 'detail', 'index']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control d-inline-block mb-2"
        self.fields['file'].widget.attrs["class"] = "px-2 pt-0 pb-3 d-block"
        self.fields['title'].widget.attrs["placeholder"] = "セットリスト テンプレート"


    def clean_index(self):
        index = self.cleaned_data.get('index')
        if index is None:
            return 0
        if index < -30000:
            raise forms.ValidationError('設定値が負に大きすぎます。設定可能な数値は-30000から30000までです。')
        if index > 30000:
            raise forms.ValidationError('設定値が大きすぎます。設定可能な数値は-30000から30000までです。')
        return index


class EditForm(UploadForm):
    delete = forms.BooleanField(
        initial=False,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'].widget.attrs["class"] = ""
