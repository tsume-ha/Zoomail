from django import forms
from .models import Calendar
import os
import datetime

class CreateCalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['title', 'text', 'days_begin', 'days_end']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['days_begin'].widget=forms.SelectDateWidget(
            years=[datetime.datetime.now().year, datetime.datetime.now().year +1]
        )
        self.fields['days_end'].widget=forms.SelectDateWidget(
            years=[datetime.datetime.now().year, datetime.datetime.now().year +1]
        )
        self.fields['text'].required = False
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class InviteUserForm(forms.Form):
    year_choice = forms.ChoiceField(# No POSTed DATA is USED in VIEW.PY, This Form is used only for JS
        label = "Year",
        required = False,
    )
    invite_user = forms.ChoiceField(
        required = False
    )
    user_post_data = forms.CharField(
        widget=forms.HiddenInput()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year_choice'].widget.attrs["class"] = "form-control"
        self.fields['invite_user'].widget.attrs["class"] = "form-control"

class InputScheduleForm(forms.Form):
    displaytime = forms.CharField(required=False)
    can_attend = forms.ChoiceField(
        widget=forms.RadioSelect(),
        required = False,
        choices = {(True, '○'),(False, '×')}
    )
    datetime = forms.DateTimeField(
        widget=forms.HiddenInput()
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['displaytime'].widget.attrs["readonly"] = "readonly"
        self.fields['displaytime'].widget.attrs["disabled"] = "True"
        self.fields['displaytime'].widget.attrs["class"] = "form-control-plaintext displaytime"