from django import forms

class SendMessage(forms.Form):
	title = forms.CharField(label="件名",widget=forms.TextInput(attrs={
		'placeholder': '件名'
		}))
	to = forms.ChoiceField(
		choices = [("error","宛先を選択してください"),(0,"全回メーリス" + "（" + now_kaisei() + "～21期）",)] + kaisei,
		label = "宛先"
	)
	attachment = forms.BooleanField(label="添付ファイル",required=False)
	content = forms.CharField(label="本文",widget=forms.Textarea(attrs={
		'placeholder': '本文を入力',
	}))
