from django import forms
# from django.core import validators
from .models import Message, Attachment
# from .to import to_groups


## new API form
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content', 'writer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    to = forms.MultipleChoiceField(
        # choices = to_groups,
        required = True
    )


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['attachment_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
