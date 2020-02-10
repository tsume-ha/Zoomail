from django import forms
from .models import Song
import os

class CreateRehasalForm(forms.Form):
    livename = forms.CharField(label="収録イベント名",widget=forms.TextInput(attrs={
        'placeholder': 'NFリハ#2',
        'class': 'form-control',
        }))
    recorded_at = forms.DateField(label="収録日",widget=forms.DateInput(attrs={
        'type': 'date',
        'placeholder': '2019-07-30',
        'class': 'form-control',
        })
        )

class CreateSongForm(forms.Form):
    song_name = forms.CharField(label="曲名",widget=forms.TextInput(attrs={
        'placeholder': '曲名 例)ノーダウト',
        'data': 'songname',
        }))
    song_file = forms.FileField(
        label = "MP3ファイルを選択してください",
        required = False,
        widget = forms.FileInput(attrs={'class':'border border-primary rounded-right'}),
    )

class EditSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['track_num', 'song_name', 'file']
