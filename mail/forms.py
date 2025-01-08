# forms.py

from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Message, Attachment, ToGroup


class MessageForm(forms.ModelForm):
    """
    Messageモデル用のフォーム
    """

    class Meta:
        model = Message
        fields = ["title", "content", "writer", "to_groups"]
        widgets = {
            "title": forms.TextInput(
                attrs={"max_length": 200, "class": "form-control"}
            ),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "writer": forms.Select(attrs={"class": "form-control"}),
            "to_groups": forms.SelectMultiple(),
        }
        labels = {
            "title": "件名",
            "content": "本文",
            "writer": "差出人",
            "to_groups": "宛先",
        }


class AttachmentForm(forms.ModelForm):
    """
    Attachmentモデル用のフォーム
    """

    class Meta:
        model = Attachment
        fields = ["file"]  # org_filenameはviewで設定する。
        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }
        labels = {
            "file": "添付ファイル",
        }

    def clean_file(self):
        """
        fileフィールドのバリデーション
        ファイルサイズが3バイト以上、10MB以下であることを確認します。
        """
        file = self.cleaned_data.get("file")
        if file:
            if file.size < 3:
                raise forms.ValidationError("ファイルサイズが0です")
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("ファイルサイズが上限(10MB)を超えています")
        else:
            raise forms.ValidationError("ファイルがアップロードされていません")
        return file


class FileInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        total_size = 0
        max_size = 30 * 1024 * 1024  # 30MB

        for form in self.forms:
            # フォームにエラーがある場合や、cleaned_data が無い場合は飛ばす
            if not hasattr(form, "cleaned_data"):
                continue

            # もし削除フラグが立っていなかったらファイルサイズを合計
            if not form.cleaned_data.get("DELETE", False):
                uploaded_file = form.cleaned_data.get("file")
                if uploaded_file:
                    total_size += uploaded_file.size

        if total_size > max_size:
            raise ValidationError(
                "アップロードできるファイルの合計サイズは30MBまでです。"
            )


AttachmentFormset = inlineformset_factory(
    parent_model=Message,
    model=Attachment,
    fields=("file",),  # 他のフィールドがあれば追加してください
    extra=1,
    can_delete=False,
    formset=FileInlineFormSet,  # カスタム Formset を指定
)


class CompositeForm(forms.Form):
    """
    1ステップ目(本文 + 添付ファイル)をまとめて処理するための「複合フォーム」。

    ただし、fields は持たず、__init__ で内部的に
    - MessageForm
    - AttachmentFormset
    を初期化して保管します。
    """

    def __init__(self, *args, **kwargs):
        # まず、WizardView から渡されるであろう "instance" (Message) や
        # POSTデータ (args[0] かもしれない) を取り出す
        self.instance = kwargs.pop(
            "instance", None
        )  # Messageインスタンス (新規 or 既存)
        super().__init__(*args, **kwargs)

        # Message用フォームを内部的に初期化
        self.message_form = MessageForm(
            data=self.data if self.is_bound else None, instance=self.instance
        )

        # Attachment用の inline formset を内部的に初期化
        self.attachment_formset = AttachmentFormset(
            data=self.data if self.is_bound else None,
            instance=self.instance,
            files=self.files if self.is_bound else None,
        )

    def is_valid(self):
        """
        この複合フォームがバリデーションOKかどうかを、
        内部の2つ (MessageForm, AttachmentFormset) に問い合わせる
        """
        return self.message_form.is_valid() and self.attachment_formset.is_valid()

    def clean(self):
        """
        もし複合的な整合性チェックが必要であればここで行う。
        ここでは特になし。
        """
        # self.message_form と self.attachment_formset の両方を参照可能
        return super().clean()

    @property
    def cleaned_data(self):
        """
        WizardView は form.cleaned_data にアクセスしてセッションへ保存するため、
        MessageForm と AttachmentFormset の cleaned_data を合体して返す。
        """
        if not self.is_valid():
            raise forms.ValidationError("CompositeForm is not valid.")

        # message_form.cleaned_data は dict
        # attachment_formset.cleaned_data はリスト(各フォームの dict)
        return {
            "message_form": self.message_form.cleaned_data,
            "attachments": [
                f.cleaned_data for f in self.attachment_formset.forms if f.cleaned_data
            ],
        }
