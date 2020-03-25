from django import forms
from .models import Calendar, Schedule, CollectHour, CalendarUser
import os
import datetime

class CreateCalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['title', 'text', 'days_begin', 'days_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.date.today()
        self.fields['days_begin'].widget = self.fields['days_end'].widget = forms.HiddenInput()
        self.fields['text'].required = False
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        days_begin = cleaned_data.get('days_begin')
        days_end = cleaned_data.get('days_end')
        if days_end < days_begin:
            raise forms.ValidationError(
                '集計終了日が、開始日よりも前になっています。'
            )
        if (days_end - days_begin).days > 120:
            raise forms.ValidationError(
                '集計できる期間は最大で120日間です。'
            )



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

    def clean(self):
        cleaned_data = super().clean()
        hour_begin = cleaned_data.get('hour_begin')
        hour_end = cleaned_data.get('hour_end')
        if not 9 <= hour_begin <= 26:
            raise forms.ValidationError(
                '開始時間は24時間表記で9時から26時までの範囲で指定してください'
            )
        if not 9 <= hour_end <= 26:
            raise forms.ValidationError(
                '終了時間は24時間表記で9時から26時までの範囲で指定してください'
            )
        if hour_end < hour_begin:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return cleaned_data

UpdateCollectHourFormSet = forms.modelformset_factory(
    CollectHour, form=UpdateCollectHourForm, extra=0,
)

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CalendarUser
        fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()



UserChangeFormSet = forms.modelformset_factory(
    CalendarUser, form=UserChangeForm, extra=0, can_delete=True,
)
