from django import forms


class SendMessage(forms.Form):
    title = forms.CharField(label="件名")
    to = forms.CharField(label="宛先")
    content = forms.CharField(label="本文",widget=forms.Textarea)