from typing import Any, Dict
from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from members.models import User
from .models import Message, Attachment, ToGroup


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title", "content", "writer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    to = forms.MultipleChoiceField(
        required=True, label="宛先グループ", widget=forms.SelectMultiple
    )


class AttachmentForm(forms.ModelForm):
    """
    ModelFormを使用してAttachmentフォームを作成
    """

    class Meta:
        model = Attachment
        fields = ["attachment_file"]

    def clean_attachment_file(self):
        file = self.cleaned_data.get("attachment_file")
        if file.size < 3:
            raise forms.ValidationError("ファイルサイズが0です")
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("ファイルサイズが上限(10MB)を超えています")
        return file


class ToGroupForm(forms.ModelForm):
    """
    宛先グループのフォーム
    """

    class Meta:
        model = ToGroup
        fields = ["year", "leader", "label"]


# フォームセットを作成
AttachmentFormSet = inlineformset_factory(
    Message,
    Attachment,
    form=AttachmentForm,
    fields=["attachment_file"],
    extra=1,
    can_delete=True,
)


# 全体をまとめたフォーム
class MailisForm(forms.Form):
    message_form = MessageForm()
    attachment_formset = AttachmentFormSet()

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)
        if instance:
            self.message_form = MessageForm(instance=instance)
            self.attachment_formset = AttachmentFormSet(instance=instance)

    def is_valid(self):
        return self.message_form.is_valid() and self.attachment_formset.is_valid()

    def save(self, commit=True):
        message = self.message_form.save(commit=commit)
        self.attachment_formset.instance = message
        self.attachment_formset.save(commit=commit)
        return message


class ToGroupAdminForm(forms.ModelForm):
    class Meta:
        model = ToGroup
        verbose_name = "宛先"
        verbose_name_plural = "宛先"
        fields = ["year", "leader", "label"]

    def clean(self) -> Dict[str, Any]:
        leader: User = self.cleaned_data.get("leader")
        if leader:
            if self.cleaned_data["year"] != leader.year:
                raise forms.ValidationError(
                    "会長に指定されたユーザーの学年が、宛先に設定された学年と一致していません。"
                )
        return super().clean()
