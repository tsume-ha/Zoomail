# views.py
import os
import uuid
import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.conf import settings

from formtools.wizard.views import SessionWizardView

from members.models import User
from ..models import Message, Attachment
from ..forms import MessageForm, AttachmentFormset, CompositeForm

# 2ステップ: "create" (入力画面), "confirm" (確認画面)
# Form Wizardには'ダミー'を割り当てている（実際のフォームは手動管理するため）
from django import forms

FORMS = [
    (
        "compose",
        CompositeForm,
    ),  # Step1: ダミーフォーム (実際にはMessageForm + AttachmentFormsetを使う)
    ("confirm", forms.Form),  # Step2: ダミーフォーム (確認画面)
]

TEMPLATES = {
    "compose": "mail/send_create.html",
    "confirm": "mail/send_confirm.html",
}


class SendWizardView(SessionWizardView):
    """
    2ステップ:
      1) compose: MessageForm + AttachmentFormset (複合フォーム)
      2) confirm: 確認用の空フォーム
    """

    form_list = FORMS
    file_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT / "tmp")

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def process_step_files(self, form):
        result = super().process_step_files(form)
        print(result)
        return result

    def get_form_kwargs(self, step=None):
        """
        inlineformset_factory には親 Message の instance が必要。
        新規作成を想定して Message() を渡す。
        """
        kwargs = super().get_form_kwargs(step)
        if step == "compose":
            # 新規の場合は空の Message インスタンスを生成して渡す
            # 既存のメッセージに添付ファイルを追加するなら、その既存Messageを渡す
            kwargs["instance"] = Message()
        return kwargs

    def render(self, form=None, **kwargs):
        """
        テンプレートへ複合フォーム内部のフォームを渡すため、context を拡張する。
        """
        if self.steps.current == "compose" and isinstance(form, CompositeForm):
            # composeステップのときだけ、message_form / attachment_formset もテンプレートに渡す
            kwargs.update(
                {
                    "message_form": form.message_form,
                    "attachment_formset": form.attachment_formset,
                }
            )
        return super().render(form=form, **kwargs)

    def done(self, form_list, **kwargs):
        """
        確認画面で「送信」された時の最終処理
        """
        # form_list[0] -> CompositeForm
        composite_form = form_list[0]

        # --- (1) MessageForm.save() の呼び出し ---
        # CompositeForm 内にある MessageForm は「message_form」という名前で格納してあるので取り出す
        message_form = composite_form.message_form

        # ここで commit=False にするのは、あとで何か追加設定を行うケースを想定しているだけで、
        # 特に追加が無いのであれば commit=True でもOKです。
        message_obj = message_form.save(commit=False)

        # もし何か追加で Message のフィールドを上書きしたいならここで行う
        # (例: message_obj.some_extra_field = "...")
        message_obj.sender = self.request.user

        message_obj.save()

        # ManyToManyField (to_groupsなど) を正しく保存するには save_m2m() が必要
        message_form.save_m2m()

        # --- (2) AttachmentFormset.save() ---
        # Attachment モデルを保存
        for attachment_form in composite_form.attachment_formset:
            attachment = attachment_form.save(commit=False)
            attachment.org_filename = attachment.file.name
            attachment.save()

        # for attach_data in composite_form.attachment_formset.cleaned_data:
        #     file_obj = attach_data.get("file", None)
        #     if file_obj:
        #         attachment = Attachment(
        #             message=message_obj,
        #             file=file_obj,
        #             org_filename=file_obj.name,
        #         )
        #         attachment.save()

        # すべて保存完了したら、適当なページへリダイレクト
        return redirect("mail:inbox")
