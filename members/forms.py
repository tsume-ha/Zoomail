from django import forms
from .models import User

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email', 'last_name', 'first_name','nickname') # changed from google_account

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

class RegistarForm(forms.Form):
    email = forms.CharField(
        label = "",
        required = True,
        widget = forms.TextInput(attrs = {
            'placeholder': 'Google Accountを入力'
        })
    )
    email = forms.IntegerField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs = {
            'placeholder': '回生を入力'
        })
    )