from django import forms
from .models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file", "filename"]

    def clean(self):
        cleaned_data = super().clean()
        uploaded_file = cleaned_data.get("file")
        if uploaded_file:
            cleaned_data["filename"] = uploaded_file.name
        return cleaned_data
