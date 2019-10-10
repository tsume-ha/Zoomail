from django import forms
from .models import Calendar, Schedule
import os

class CreateCalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['title', 'text', 'days_begin', 'days_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['days_begin'].widget=forms.SelectDateWidget()
        self.fields['days_end'].widget=forms.SelectDateWidget()
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class InviteUserForm(forms.From):
    year_choice = forms.ChoiceField(# No POSTed DATA is USED in VIEW.PY, This Form is used only for JS
        label = "From"
    )
    written_by = forms.ChoiceField(
        label = "送信元",
    )
    def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs["class"] = "form-control"

class InputScheduleForm(forms.Form):
    can_attend = forms.BooleanField(
    	widget=forms.RadioSelect(
    		attrs={'class': 'form-control'},
    		),
        required = False,
    )