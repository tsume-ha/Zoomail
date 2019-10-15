from django import forms
from django.forms.utils import ErrorList
from django.core import validators
from .models import User



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'furigana', 'nickname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['nickname'].required = False

    def get_object(self):
        return self.request.user



class RegisterForm(forms.Form):
    email = forms.EmailField(
        label = "",
        required = True,
        widget = forms.TextInput(attrs = {
            'placeholder': 'Google Accountを入力',
            'class': 'form-control m-2',
        })
    )
    year = forms.IntegerField(
        label = "",
        required = True,
        widget = forms.NumberInput(attrs = {
            'placeholder': '入部年度を入力（例：2019）',
            'class': 'form-control m-2',
        })
    )
    last_name = forms.CharField(
        label = "",
        required = True,
        widget = forms.TextInput(attrs = {
            'placeholder': '苗字',
            'class': 'form-control col-sm-5 m-2',
        })
    )
    first_name = forms.CharField(
        label = "",
        required = True,
        widget = forms.TextInput(attrs = {
            'placeholder': '名前',
            'class': 'form-control col-sm-5 m-2',
        })
    )
    furigana = forms.CharField(
        label = "",
        required = True,
        widget = forms.TextInput(attrs = {
            'placeholder': 'ふりがな',
            'class': 'form-control m-2',
        }),
        validators=[validators.RegexValidator(
            regex=u'^[ぁ-ん]+$',
            message='ふりがなは全角ひらがなのみで入力してください。',
        )]
    )

    def clean_year(self):
        year = self.cleaned_data['year']
        if not ( year == 0 or 1990 < year < 2100 ):
            raise forms.ValidationError('無効な入部年度です。第24期などでなく、入部年度（2018）を入力してください。')
        return year


class RegisterCSV(forms.Form):
    csv_file = forms.FileField(
    	label="",
    	required =True,
    	)
		