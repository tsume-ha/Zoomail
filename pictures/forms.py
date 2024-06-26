from django import forms
from django.core import validators
from .models import Album
import datetime


class AlbumRegisterForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["title", "held_at", "url", "thumbnail"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["held_at"].initial = datetime.date.today()
        self.fields["held_at"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )
        self.fields["thumbnail"].widget = forms.FileInput(attrs={"placeholder": "サムネイル画像"})
        self.fields["thumbnail"].required = False
