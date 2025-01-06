# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

from formtools.wizard.views import SessionWizardView

from ..models import Message, Attachment
from ..forms import MessageForm, AttachmentFormset

# 2ステップ: "create" (入力画面), "confirm" (確認画面)
# Form Wizardには'ダミー'を割り当てている（実際のフォームは手動管理するため）
from django import forms

FORMS = [
    (
        "create",
        forms.Form,
    ),  # Step1: ダミーフォーム (実際にはMessageForm + AttachmentFormsetを使う)
    ("confirm", forms.Form),  # Step2: ダミーフォーム (確認画面)
]

TEMPLATES = {
    "create": "mail/send_create.html",
    "confirm": "mail/send_confirm.html",
}


@method_decorator(require_http_methods(["GET", "POST"]), name="dispatch")
class SendWizardView(SessionWizardView):
    """
    2ステップのフォームウィザード
    Step1: 作成画面 (MessageForm + AttachmentFormset)
    Step2: 確認画面
    """

    form_list = FORMS

    def get_template_names(self):
        """
        ステップごとに使うテンプレートを切り替え
        """
        return [TEMPLATES[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        """
        各ステップで必要なフォームや表示用データをコンテキストに渡す
        """
        context = super().get_context_data(form=form, **kwargs)

        if self.steps.current == "create":
            # Step1 (GET or POST) -> MessageForm, AttachmentFormset の作成
            if self.request.method == "POST":
                # WizardViewの内部的には "form" はダミーフォームなので、自力でバリデーション
                context["message_form"] = MessageForm(self.request.POST)
                context["attachment_formset"] = AttachmentFormset(
                    self.request.POST, self.request.FILES, prefix="attachment"
                )
            else:
                # GET の場合
                context["message_form"] = MessageForm()
                context["attachment_formset"] = AttachmentFormset(prefix="attachment")

        elif self.steps.current == "confirm":
            # Step2 -> Step1の入力値を読み出して表示する
            # WizardViewのstorageに一時保存してあるデータを取り出し
            stored_data = self.storage.extra_data.get("step1_data")
            if stored_data:
                context["message_form_data"] = stored_data.get("message_form_data")
                context["attachment_form_data"] = stored_data.get(
                    "attachment_form_data"
                )
            else:
                # 何もなければ空
                context["message_form_data"] = {}
                context["attachment_form_data"] = []

        return context

    def render_next_step(self, form, **kwargs):
        """
        次のステップへ遷移する際に、Step1のバリデーション結果をチェック。
        AttachmentFormset がエラーなら同じステップに留まる。
        さらに writer を pk に変換する。
        """
        if self.steps.current == "create":
            # POSTデータから自力でバリデーション
            message_form = MessageForm(self.request.POST)
            attachment_formset = AttachmentFormset(
                self.request.POST, self.request.FILES, prefix="attachment"
            )

            if not (message_form.is_valid() and attachment_formset.is_valid()):
                # バリデーション失敗 -> 同じステップに留まる
                return self.render(
                    self.get_form(step="create"),
                    context={
                        "message_form": message_form,
                        "attachment_formset": attachment_formset,
                    },
                )
            else:
                # バリデーション成功 -> データを storage に保存し、confirm 画面へ進む
                cleaned_data = message_form.cleaned_data.copy()

                # --- ここで writer が Userオブジェクトなら pk に置き換える ---
                writer_obj = cleaned_data.get("writer")
                if writer_obj:
                    cleaned_data["writer"] = writer_obj.pk

                # --- ここで to_groups が QuerySetなら pk リストに変換 ---
                groups_qs = cleaned_data.get("to_groups")
                if groups_qs:
                    cleaned_data["to_groups"] = [g.pk for g in groups_qs]

                self.storage.extra_data["step1_data"] = {
                    "message_form_data": cleaned_data,
                    "attachment_form_data": [
                        f.cleaned_data
                        for f in attachment_formset
                        if f.cleaned_data and not f.cleaned_data.get("DELETE", False)
                    ],
                }
        return super().render_next_step(form, **kwargs)

    def done(self, form_list, **kwargs):
        """
        「確認画面」から最終的に「送信」ボタンが押されたら呼ばれる
        -> データベースへの保存処理を実行
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()

        step1_data = self.storage.extra_data.get("step1_data", {})
        message_form_data = step1_data.get("message_form_data", {})
        attachment_form_data = step1_data.get("attachment_form_data", [])

        # writer_pk を取り出して User オブジェクトに戻す
        writer_pk = message_form_data.get("writer")
        writer_user = None
        if writer_pk:
            writer_user = User.objects.get(pk=writer_pk)

        # Message モデルを保存
        message = Message(
            writer=writer_user,  # PKから取得したUserオブジェクト
            title=message_form_data.get("title", ""),
            content=message_form_data.get("content", ""),
            # 他に必要なフィールドがあれば加える
        )
        message.save()

        # ManyToMany (to_groups) があれば同様に set() などで紐づけ
        groups_pk_list = message_form_data.get("to_groups", [])
        message.to_groups.set(groups_pk_list)

        # Attachment モデルを保存
        for attach_data in attachment_form_data:
            file_obj = attach_data.get("file", None)
            if file_obj:
                attachment = Attachment(
                    message=message,
                    file=file_obj,
                    org_filename=file_obj.name,
                )
                attachment.save()

        messages.success(self.request, "メッセージが正常に作成されました。")

        # 終了後は受信箱などにリダイレクト
        return redirect("mail:inbox")
