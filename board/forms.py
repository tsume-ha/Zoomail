from django import forms
import datetime

kaisei = [
(2019,"2019 25期",),
(2018,"2018 24期（会長 : 成基人）",),
(2017,"2017 23期（会長 : 宮武功貴）",),
(2016,"2016 22期（会長 : 木内幹也）",),
(2015,"2015 21期（会長 : 飯干歩）",),
]

def now_kaisei():
	year = datetime.datetime.now().year
	return str(year - 1994) + "期"

class SendMessage(forms.Form):
	title = forms.CharField(label="件名")
	to = forms.ChoiceField(
		choices = [(0,"全回メーリス" + "（" + now_kaisei() + "～21期）",)] + kaisei,
		label = "宛先",
	)
	attachment = forms.BooleanField(label="添付ファイル",)
	content = forms.CharField(label="本文",widget=forms.Textarea)

