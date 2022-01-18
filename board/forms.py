from distutils.command.clean import clean
from tkinter.messagebox import RETRY
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
        self.fields["attachment_file"].required=False
        self.fields["attachment_file"].allow_empty_file=False
        self.fields["attachment_file"].widget.attrs = { "multiple": True }

    # def clean_attachment_file(self):
    #     files = self.cleaned_data["attachment_file"]
    #     print(files.size)
    #     return files