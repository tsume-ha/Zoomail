from django import forms
from .models import Messages, Message_Year, Message_Attachment, Message_Tag


# class SendMessage(forms.Form):
# 	title = forms.CharField(label="件名")
# 	to = forms.ChoiceField(
# 		choices = [("全回メーリス","全回メーリス",),("Public","Public",),],
# 		label = "宛先",
# 		)
# 	content = forms.CharField(label="本文",widget=forms.Textarea)

# class SendTo(forms.Form):
# 	to = forms.ChoiceField(
# 		choices = [("全回メーリス","全回メーリス",),("Public","Public",),],
# 		label = "宛先",
# 		)

class SendMessage(forms.ModelForm):
	class Meta:
		model = Messages
		exclude = ['sender_id', 'writer_id', 'created_at', 'updated_at']

class SendTo(forms.ModelForm):
	class Meta:
		model = Message_Year
		exclude = ['mes_ID']
			