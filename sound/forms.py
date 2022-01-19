import os

from django import forms

from .models import Song


class CreateRehasalForm(forms.Form):
    livename = forms.CharField(
        label="収録イベント名",
        widget=forms.TextInput(attrs={"placeholder": "NFリハ#2", "class": "form-control", "v-model": "livename"}),
        required=True,
    )
    recorded_at = forms.DateField(
        label="収録日",
        widget=forms.HiddenInput(
            attrs={
                "v-bind:value": "recorded_at",
            }
        ),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()


class EditSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["track_num", "song_name", "file"]

    def clean(self):
        cleaned_data = super().clean()
