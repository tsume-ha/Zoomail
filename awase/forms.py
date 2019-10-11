from django import forms
from .models import Calendar
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

class InviteUserForm(forms.Form):
    year_choice = forms.ChoiceField(# No POSTed DATA is USED in VIEW.PY, This Form is used only for JS
        label = "Year"
    )
    invite_user = forms.ChoiceField(
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year_choice'].widget.attrs["class"] = "form-control"
        self.fields['invite_user'].widget.attrs["class"] = "form-control"

class InputScheduleForm(forms.Form):
    can_attend = forms.BooleanField(
        widget=forms.RadioSelect(
            attrs={'class': 'form-control'},
            ),
        required = False,
    )