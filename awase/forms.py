from django import forms
from .models import Calendar, Schedule, CollectHour
import os
import datetime

class CreateCalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['title', 'text', 'days_begin', 'days_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.date.today()
        self.fields['days_begin'].widget = self.fields['days_end'].widget = forms.SelectDateWidget(
            years=[today.year, today.year +1]
        )
        self.fields['days_begin'].initial = today
        self.fields['days_end'].initial = today + datetime.timedelta(days=60)
        self.fields['text'].required = False
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class InputScheduleForm(forms.Form):
    displaytime = forms.CharField(required=False)
    can_attend = forms.ChoiceField(
        widget=forms.RadioSelect(),
        required = False,
        choices = {(True, '○'),(False, '×')}
    )
    starttime = forms.DateTimeField(
        widget=forms.HiddenInput()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['displaytime'].widget.attrs["readonly"] = "readonly"
        self.fields['displaytime'].widget.attrs["disabled"] = "True"
        self.fields['displaytime'].widget.attrs["class"] = "form-control-plaintext displaytime"

InputScheduleFormSet = forms.formset_factory(
    InputScheduleForm, extra=0
)


class UpdateCollectHourForm(forms.ModelForm):
    class Meta:
        model = CollectHour
        fields = ['date', 'hour_begin', 'hour_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.HiddenInput()
        self.fields['hour_begin'].widget.attrs["class"] = "form-control col-3 mx-2"
        self.fields['hour_end'].widget.attrs["class"] = "form-control col-3 mx-2"

    def clean_hour_begin(self):
        hour_begin = self.cleaned_data['hour_begin']
        if not 9 <= hour_begin <= 26:
            raise forms.ValidationError(
                '24時間表記で9時から26時までの範囲で指定してください'
            )
        return hour_begin

    def clean_hour_end(self):
        hour_end = self.cleaned_data['hour_end']
        if not 9 <= hour_end <= 26:
            raise forms.ValidationError(
                '24時間表記で9時から26時までの範囲で指定してください'
            )
        return hour_end

    def clean(self):
        hour_begin = self.cleaned_data['hour_begin']
        hour_end = self.cleaned_data['hour_end']
        if hour_end < hour_begin:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )

UpdateCollectHourFormSet = forms.modelformset_factory(
    CollectHour, form=UpdateCollectHourForm, extra=0,
)