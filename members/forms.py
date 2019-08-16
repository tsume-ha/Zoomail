from django import forms
from .models import User

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('google_account', 'last_name', 'first_name', 'nickname', 'furigana')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'