from django import forms
import os

class CreateRehasalForm(forms.Form):
	livename = forms.CharField(label="収録イベント名",widget=forms.TextInput(attrs={
		'placeholder': 'NFリハ#2',
		'class': 'form-control',
		}))
	recorded_at = forms.DateField(label="収録日",widget=forms.TextInput(attrs={
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
		# validators = [validate_is_MP3],
		required = False,
	)

	# def validate_is_MP3(value):
	# 	ext = os.path.splitext(value.name)[1]

	# 	if not ext.lower() in ['.mp3',]:
	# 		raise ValidationError('Only mp3 audio files are availables.')



