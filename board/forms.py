from django import forms
from .models import Message, Attachment


## new API form
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title", "content", "writer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    to = forms.MultipleChoiceField(required=True)


class AttachmentForm(forms.Form):
    """
    ModelFormではなく通常のFormであることに注意
    save()のみ独自実装
    """

    attachments = forms.FileField(
        required=False, allow_empty_file=False, widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    def clean_attachments(self):
        files = self.files.getlist("attachments")
        total_file_size = 0
        for file in files:
            if file.size < 3:
                raise forms.ValidationError("ファイルサイズが0です")
            if file.size > 10 * 1000 * 1000:
                raise forms.ValidationError("ファイルサイズが上限(10MB)を超えています")
            total_file_size += file.size
        if total_file_size > 20 * 1024 * 1024:
            raise forms.ValidationError("合計のファイルサイズが上限(20MB)を超えています")
        return files

    def save(self, message: Message):
        files = self.cleaned_data["attachments"]
        return [Attachment.objects.create(message=message, attachment_file=file) for file in files]
