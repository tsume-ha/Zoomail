from django import forms
from .models import Kansouyoushi
import datetime


class KansouUploadForm(forms.ModelForm):
    livename = [
    ('sinkanlive','新歓ライブ'),
    ('junelive','6月ライブ'),
    ('freshmanlive','新人ライブ'),
    ('septemberlive','9月ライブ'),
    ('octoberlive','10月ライブ'),
    ('christmaslive','クリスマスライブ'),
    ('newyearlive','あけおめライブ'),
    ('marchlive','3月ライブ'),
    ('other','その他'),
    ]

    class Meta:
        model = Kansouyoushi
        fields = ['live', 'performed_at', 'numbering', 'file', 'detail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['live'] = forms.ChoiceField(
            choices = self.livename,
            label = "ライブ名",
            widget = forms.Select(attrs={'class': 'form-control'}),
            required = True,
            )
        self.fields['file'].widget.attrs["class"] = "m-2"
        self.fields['detail'].required = False
        self.fields['detail'].widget.attrs['placeholder'] = '例）1回生の分です'
        self.fields['numbering'].required = False
        self.fields['performed_at'].initial = datetime.date.today()
        self.fields['performed_at'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control',})


    def clean_numbering(self):
        numbering = self.cleaned_data['numbering']
        if numbering == None:
            numbering = 1
        return numbering

    def clean(self):
        cleaned_data = super().clean()
        performed_at = cleaned_data.get("performed_at")
        livename = cleaned_data.get("live")
        file = cleaned_data.get("file")
        numbering = cleaned_data.get('numbering')
        filename = performed_at.strftime('%Y_%m_%d') + '_' + livename
        if numbering != None:
            filename += '_' + str(numbering)
        filename += '.pdf'
        file.name = filename
        return cleaned_data