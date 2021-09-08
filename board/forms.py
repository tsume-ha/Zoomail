from django import forms
from .models import Message, Attachment


## new API form
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content', 'writer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    to = forms.MultipleChoiceField(
        required = True
    )


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['attachment_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
