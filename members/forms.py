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