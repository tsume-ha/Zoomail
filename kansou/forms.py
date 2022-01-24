from django import forms
from .models import Kansouyoushi
import datetime


class KansouUploadForm(forms.ModelForm):
    class Meta:
        model = Kansouyoushi
        fields = ["title", "performed_at", "file", "detail"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["title"].widget.attrs["placeholder"] = "例）新歓ライブ#1"
        self.fields["file"].widget.attrs["class"] = "m-2"
        self.fields["detail"].required = False
        self.fields["detail"].widget.attrs["placeholder"] = "例）1回生の分です"
        self.fields["performed_at"].initial = datetime.date.today()
        self.fields["performed_at"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )

    def clean(self):
        cleaned_data = super().clean()
        performed_at = cleaned_data.get("performed_at")
        file = cleaned_data.get("file")
        filename = performed_at.strftime("%Y_%m_%d_%M_%S")
        filename += ".pdf"
        file.name = filename
        return cleaned_data
