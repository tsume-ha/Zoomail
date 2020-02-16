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
        self.fields['date'].widget = forms.DateInput(
            format = '%m/%d',
            attrs = {
                'readonly': 'readonly',
                'disabled': 'True',
                'class': 'form-control-plaintext displaytime',
            })
        self.fields['date'].required = False
        
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


UpdateCollectHourFormSet = forms.modelformset_factory(
    CollectHour, form=UpdateCollectHourForm, extra=0,
)