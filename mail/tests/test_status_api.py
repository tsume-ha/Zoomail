import json
import urllib.request
import urllib.parse
import urllib.error

from django.urls import reverse
from django.conf import settings
from django.test import TestCase, Client, override_settings

from enum import Enum
from mail.models import MailLog


class Status(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


def is_message_to_be_sent(message_id: str, endpoint: str, api_key: str, urlopen_func):
    url = f"{endpoint}?message_id={message_id}"
    req = urllib.request.Request(url, headers={"X-Authorization": api_key})
    try:
        with urlopen_func(req) as response:
            data = json.loads(response.read().decode())
            status = Status(data["status"])
            if status == Status.PENDING or status == Status.FAILED:
                return True
            elif status == Status.SUCCESS:
                return False
            else:
                print(f"Invalid Status: {message_id}, Status: {status}")
                return False
    except urllib.error.URLError as e:
        print(f"Error occurred while checking message status: {e}")
        return None


def update_message_status(
    message_id: str, status: Status, endpoint: str, api_key: str, urlopen_func
):
    data_dict = {
        "message_id": message_id,
        "status": status.value,
    }
    if status == Status.FAILED:
        data_dict["error_message"] = "error occurred"
    data_encoded = urllib.parse.urlencode(data_dict).encode()
    req = urllib.request.Request(
        endpoint, data=data_encoded, headers={"X-Authorization": api_key}
    )
    try:
        with urlopen_func(req) as response:
            data = json.loads(response.read().decode())
            response_status = Status(data["status"])
            assert response_status == status
            return
    except Exception as e:
        print(e)
        return None


@override_settings(MAIL_STATUS_API_KEY="testkey")
class MailStatusApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        # テスト用に MailLog レコードを作成（必須フィールド email を含む）
        self.mail_log = MailLog.objects.create(
            mail_id="12345", status="pending", error="", email="test@example.com"
        )
        # API のエンドポイントと API キーを設定
        path = reverse("mail_status_api")
        # Django のテストクライアントはデフォルトで testserver ホスト
        self.api_endpoint = f"http://testserver{path}"
        self.api_key = settings.MAIL_STATUS_API_KEY

    def fake_urlopen(self, req):
        # Django の test client を利用して、req に応じたリクエストを送信する
        if getattr(req, "data", None) is None:
            # GET リクエストの場合
            response = self.client.get(req.full_url, HTTP_X_AUTHORIZATION=self.api_key)
        else:
            # POST リクエストの場合
            parsed = urllib.parse.parse_qs(req.data.decode())
            # flatten the parsed dict (values are lists)
            data = {k: v[0] for k, v in parsed.items()}
            response = self.client.post(
                req.full_url, data, HTTP_X_AUTHORIZATION=self.api_key
            )

        # ラップして、read() メソッドで内容を返すオブジェクトにする
        class FakeResponse:
            def __init__(self, content):
                self.content = content

            def read(self):
                return self.content

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        return FakeResponse(response.content)

    def test_get_without_auth(self):
        # 認証ヘッダーがない場合、Forbidden が返る
        response = self.client.get(f"{self.api_endpoint}?message_id=12345")
        self.assertEqual(response.status_code, 403)

    def test_get_without_message_id(self):
        # message_id パラメーターがない場合 BadRequest が返る
        response = self.client.get(self.api_endpoint, HTTP_X_AUTHORIZATION=self.api_key)
        self.assertEqual(response.status_code, 400)

    def test_get_non_existent_mail(self):
        # 存在しない message_id の場合 BadRequest が返る
        response = self.client.get(
            f"{self.api_endpoint}",
            data={"message_id": "nonexistent"},
            HTTP_X_AUTHORIZATION=self.api_key,
        )
        self.assertEqual(response.status_code, 400)

    def test_get_success(self):
        # 正常なGETリクエストの場合、JSONレスポンスが返る
        response = self.client.get(
            f"{self.api_endpoint}?message_id=12345", HTTP_X_AUTHORIZATION=self.api_key
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data["message_id"], self.mail_log.mail_id)
        self.assertEqual(data["status"], self.mail_log.status)

    def test_post_without_auth(self):
        # 認証ヘッダーがない場合、Forbidden が返る
        response = self.client.post(
            f"{self.api_endpoint}", {"message_id": "12345", "status": "sent"}
        )
        self.assertEqual(response.status_code, 403)

    def test_post_missing_params(self):
        # 必須パラメーターが不足している場合、BadRequest が返る
        response = self.client.post(
            f"{self.api_endpoint}",
            {"message_id": "12345"},
            HTTP_X_AUTHORIZATION=self.api_key,
        )
        self.assertEqual(response.status_code, 400)

    def test_post_non_existent_mail(self):
        # 存在しない message_id の場合、BadRequest が返る
        response = self.client.post(
            f"{self.api_endpoint}",
            {"message_id": "nonexistent", "status": "sent"},
            HTTP_X_AUTHORIZATION=self.api_key,
        )
        self.assertEqual(response.status_code, 400)

    def test_post_success(self):
        # 正常なPOSTリクエストの場合、MailLog レコードが更新され、JSONレスポンスが返る
        response = self.client.post(
            f"{self.api_endpoint}",
            {"message_id": "12345", "status": "sent", "error_message": "none"},
            HTTP_X_AUTHORIZATION=self.api_key,
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data["message_id"], self.mail_log.mail_id)
        self.assertEqual(data["status"], "sent")
        # データベースのレコードが更新されているか確認
        self.mail_log.refresh_from_db()
        self.assertEqual(self.mail_log.status, "sent")
        self.assertEqual(self.mail_log.error, "none")

    def test_client_flow(self):
        # クライアント利用シナリオ:
        # 1. 初回GETで現在のステータスを確認（初期値は "pending"）
        # 2. POSTリクエストでステータスを "sent" に更新
        # 3. 再度GETで更新後のステータスを確認
        response = self.client.get(
            f"{self.api_endpoint}?message_id=12345", HTTP_X_AUTHORIZATION=self.api_key
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data["status"], "pending")

        response = self.client.post(
            f"{self.api_endpoint}",
            {"message_id": "12345", "status": "sent", "error_message": "none"},
            HTTP_X_AUTHORIZATION=self.api_key,
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data["status"], "sent")

        response = self.client.get(
            f"{self.api_endpoint}?message_id=12345", HTTP_X_AUTHORIZATION=self.api_key
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data["status"], "sent")

    def test_client_is_message_to_be_sent(self):
        # is_message_to_be_sent をテストする
        # 現在のステータスは "pending" のため True を返すはず
        result = is_message_to_be_sent(
            "12345", self.api_endpoint, self.api_key, self.fake_urlopen
        )
        self.assertTrue(result)

        # ステータスを "success" に更新してテスト
        self.mail_log.status = "success"
        self.mail_log.save()
        result = is_message_to_be_sent(
            "12345", self.api_endpoint, self.api_key, self.fake_urlopen
        )
        self.assertFalse(result)

        # ステータスを "failed" に更新してテスト
        self.mail_log.status = "failed"
        self.mail_log.save()
        result = is_message_to_be_sent(
            "12345", self.api_endpoint, self.api_key, self.fake_urlopen
        )
        self.assertTrue(result)

    def test_client_update_message_status(self):
        # update_message_status をテストする
        # 現在のレコードは "failed" になるはず（エラー情報付き）
        update_message_status(
            "12345", Status.FAILED, self.api_endpoint, self.api_key, self.fake_urlopen
        )
        self.mail_log.refresh_from_db()
        self.assertEqual(self.mail_log.status, "failed")
        # error は "error occurred" と設定される
        self.assertEqual(self.mail_log.error, "error occurred")

        # 次に "success" に更新し、エラーなしで更新されることをテst
        update_message_status(
            "12345", Status.SUCCESS, self.api_endpoint, self.api_key, self.fake_urlopen
        )
        self.mail_log.refresh_from_db()
        self.assertEqual(self.mail_log.status, "success")
