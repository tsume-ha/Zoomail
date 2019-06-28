from django import forms


class SendMessage(forms.Form):
	title = forms.CharField(label="件名")
	to = forms.ChoiceField(
		choices = [("全回メーリス","全回メーリス",),("Public","Public",),],
		label = "宛先",
		)
	content = forms.CharField(label="本文",widget=forms.Textarea)

class SendTo(forms.Form):
	to = forms.ChoiceField(
		choices = [("全回メーリス","全回メーリス",),("Public","Public",),],
		label = "宛先",
		)
